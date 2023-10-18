## Removing extra print statements
import os
import uuid
import string
from dotenv import load_dotenv
from langchain.document_loaders import CSVLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.base import BaseCallbackHandler
import datetime
from threading import Thread
from queue import Queue
import sys
import sounddevice as sd
import soundfile as sf
import string
import asyncio
import nest_asyncio
import faiss
from sentence_transformers import SentenceTransformer

nest_asyncio.apply()
from stream_text_to_audio import stream_text_to_audio

sys.path.append("./components")
sys.path.append("./constants")
from speech_to_text import transcribe_stream
from filler_mapping import classify_and_play_audio, refresh_learning_data

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
PLAYHT_API_KEY = os.environ.get("PLAYHT_API_KEY")
PLAYHT_USER_ID = os.environ.get("PLAYHT_USER_ID")
CSV_FILE_PATH = os.environ.get("CSV_FILE_PATH")

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["PLAYHT_API_KEY"] = PLAYHT_API_KEY
os.environ["PLAYHT_USER_ID"] = PLAYHT_USER_ID

# sys.path.append("./components")


class DictionaryCallback(BaseCallbackHandler):
    def __init__(self, q):
        self.q = q
        self.words_list = []
        self.loop = asyncio.new_event_loop()
        self.thread = Thread(target=self.start_loop, args=(self.loop,))
        self.thread.start()

        self.phrases_dict = {
            "That 's great to hear!": "Thatsgreattohear.wav",
            "The Google Pixel phones are an excellent choice.": "TheGooglePixelphonesareanexcellentchoice.wav",
            "They offer a fantastic camera experience and a pure Android operating system.": "TheyofferafantasticcameraexperienceandapureAndroidoperatingsystem.wav",
            "Is there anything specific you 're looking for in a smartphone?": "Isthereanythingspecificyourelookingforinasmartphone.wav",
            "Absolutely!": "Absolutely.wav",
            "Camera quality is one of the standout features of Google Pixel phones.": "CameraqualityisoneofthestandoutfeaturesofGooglePixelphones.wav",
            "They are known for their exceptional camera capabilities, especially in low -light conditions.": "Theyareknownfortheirexceptionalcameracapabilitiesespeciallyinlowlightconditions.wav",
            "The Google Pixel 6, in particular, comes with a 50 megapixel main camera and Google 's Night Sight technology, which ensures clear and vibrant photos even in challenging lighting situations.": "TheGooglePixel6inparticularcomeswitha50megapixelmaincameraandGooglesNightSighttechnologywhichensuresclearandvibrantphotoseveninchallenginglightingsituations.wav",
            "If camera quality is a top priority for you, the Google Pixel 6 would be an excellent choice.": "IfcameraqualityisatoppriorityforyoutheGooglePixel6wouldbeanexcellentchoice.wav",
            "Would you like to book an appointment to visit our showroom and experience the Google Pixel 6 firsthand?": "WouldyouliketobookanappointmenttovisitourshowroomandexperiencetheGooglePixel6firsthand.wav",
            "That 's great to hear!": "Thatsgreattohear.wav",
            "We have a wide range of Google Pixel phones available in our store.": "WehaveawiderangeofGooglePixelphonesavailableinourshowroom.wav",
            "When would you like to visit us?": "Whenwouldyouliketovisitus.wav",
            "Can I have your name and contact number to schedule an appointment for you?": "CanIhaveyournameandcontactnumbertoscheduleanappointmentforyou.wav",
            "Great, John!": "GreatJohn.wav",
            "Thank you for providing your name and contact number.": "Thankyouforprovidingyournameandcontactnumber.wav",
            "I have scheduled an appointment for you to visit our shop and experience the Google Pixel phones firsthand.": "IhavescheduledanappointmentforyoutovisitourshopandexperiencetheGooglePixelphonesfirsthand.wav",
            "Our team at Gadget Hub is excited to assist you in finding the perfect phone with excellent camera quality.": "OurteamatGadgetHubisexcitedtoassistyouinfindingtheperfectphonewithexcellentcameraquality.wav",
            "We look forward to seeing you soon!": "Welookforwardtoseeingyousoon.wav",
            "Have a great day!": "Haveagreatday.wav",
            'Great!': 'Great.wav',
            'I can definitely help you with that.': 'Icandefinitelyhelpyouwiththat.wav',
            'What specific features are you looking for in a phone?': 'Whatspecificfeaturesareyoulookingforinaphone.wav',
            'The Google Pixel is known for its exceptional camera quality.': 'TheGooglePixelisknownforitsexceptionalcameraquality.wav',
            'It has a high-resolution camera that captures stunning photos with great detail and vibrant colors.': 'Ithasahighresolutioncamerathatcapturesstunningphotoswithgreatdetailandvibrantcolors.wav',
            "You 'll be able to take professional-looking photos with ease.": 'Youllbeabletotakeprofessionallookingphotoswithease.wav',
            'Would you like to visit our showroom to experience the camera firsthand?': 'Wouldyouliketovisitourshowroomtoexperiencethecamerafirsthand.wav',
            'Can I have your name and contact number to schedule an appointment for you to visit our shop?': 'CanIhaveyournameandcontactnumbertoscheduleanappointmentforyoutovisitourshop.wav',
            "I 'd be happy to help you find the perfect phone.": 'Idbehappytohelpyoufindtheperfectphone.wav',
            "Do you have any specific features in mind that you 're looking for in a phone, or are you open to suggestions?": 'Doyouhaveanyspecificfeaturesinmindthatyourelookingforinaphoneorareyouopentosuggestions.wav',
            'It has a high-resolution camera with advanced features like Night Sight and Portrait Mode.': 'IthasahighresolutioncamerawithadvancedfeatureslikeNightSightandPortraitMode.wav', 
            "You 'll be able to capture stunning photos and videos with great clarity and detail.": 'Youllbeabletocapturestunningphotosandvideoswithgreatclarityanddetail.wav',
            'Thank you, John.': 'ThankyouJohn.wav',
            "I 've scheduled your personal demo for this Saturday.": 'IvescheduledyourpersonaldemoforthisSaturday.wav',
            "If you have any questions, please don 't hesitate to contact us.": 'Ifyouhaveanyquestionspleasedonthesitatetocontactus.wav',
            'Have a great day!': 'Haveagreatday.wav',
            "I 'm glad to hear that you're interested in purchasing a new phone.": 'Imgladtohearthatyoureinterestedinpurchasinganewphone.wav',
            'The Google Pixel is an excellent choice.': 'TheGooglePixelisanexcellentchoice.wav',
            'Can you please let me know what specific features you are looking for in a phone?': 'Canyoupleaseletmeknowwhatspecificfeaturesyouarelookingforinaphone.wav',
            'This will help me provide you with the best recommendations and information.': 'Thiswillhelpmeprovideyouwiththebestrecommendationsandinformation.wav',
            'I understand that you are mainly concerned about the quality of the camera.': 'Iunderstandthatyouaremainlyconcernedaboutthequalityofthecamera.wav',
            'The Google Pixel phones are known for their exceptional camera capabilities.': 'TheGooglePixelphonesareknownfortheirexceptionalcameracapabilities.wav',
            'They have advanced camera features like Night Sight, which allows you to capture stunning low-light photos, and Portrait Mode, which creates professional-looking photos with a blurred background effect.': 'TheyhaveadvancedcamerafeatureslikeNightSightwhichallowsyoutocapturestunninglowlightphotosandPortraitModewhichcreatesprofessionallookingphotoswithablurredbackgroundeffect.wav',
            "If you 're interested, I would recommend visiting our shop to experience the Google Pixel's camera firsthand.": 'IfyoureinterestedIwouldrecommendvisitingourshoptoexperiencetheGooglePixelscamerafirsthand.wav',
            'Would you like to schedule an appointment?': 'Wouldyouliketoscheduleanappointment.wav',
            'Great choice!': 'Greatchoice.wav',
            "We 'd be happy to give you a hands-on demo.": 'Wedbehappytogiveyouahandsondemo.wav',
            'Please let me know your name and contact number so that I can book an appointment for you.': 'PleaseletmeknowyournameandcontactnumbersothatIcanbookanappointmentforyou.wav', 
        }
        self.is_answer_finished = False
        self.timeout = 0.2  # Set your desired timeout value in seconds
        self.timer = None

        # Initialize the sentence transformer model
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        
        # Create embeddings for your phrases and store them in a FAISS index
        self.phrase_embeddings = self.model.encode(list(self.phrases_dict.keys()))
        self.index = faiss.IndexFlatL2(self.phrase_embeddings.shape[1])
        self.index.add(self.phrase_embeddings)

    def start_loop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    async def play_audio_async(self, file_id):
        file_path = f"components/audio_files_pixel/{file_id}"
        if os.path.exists(file_path):
            data, samplerate = sf.read(file_path)
            sd.play(data, samplerate)
            sd.wait()
        else:
            print(f"Error: {file_path} does not exist")

    async def stream_audio_playht(self, text):
        # Use the stream_text_to_audio function to stream the text
        stream_text_to_audio(
            text, os.environ.get("PLAYHT_API_KEY"), os.environ.get("PLAYHT_USER_ID")
        )

    async def search_and_play_audio(self, combined_words):
        if self.is_answer_finished:  # Check whether the answer is finished or not
            print("Answer is finished. Not matching.")
            return

        # Search for the most similar phrase in the FAISS index
        query_embedding = self.model.encode([combined_words])
        D, I = self.index.search(query_embedding, k=1)
        distance = D[0][0]
        similarity = 1 - distance  # Convert distance to similarity

        if similarity > 0.7:  # Check if similarity is more than 70%
            closest_phrase = list(self.phrases_dict.keys())[I[0][0]]
            audio_file_id = self.phrases_dict.get(closest_phrase)
            
            # Print the matched sentence and its similarity score
            print(f"Matched Sentence: {closest_phrase}")
            print(f"Similarity Score: {similarity:.2f}")
            
            if audio_file_id:
                print(f"Match found for: {combined_words}")
                # await self.play_audio_async(f"{audio_file_id}")
                self.words_list.clear()
            else:
                print(f"No match found for: {combined_words}")
   
        else:
            print(f"No match found for: {combined_words}")
            

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        if self.timer:
            self.timer.cancel()
        self.is_answer_finished = False
        self.q.put(token)
        stripped_token = token.strip()

        if not self.words_list:
            self.words_list.append(stripped_token)
        else:
            if stripped_token in string.punctuation:
                self.words_list.append(stripped_token)
            else:
                separator = " "
                self.words_list.append(separator + stripped_token)

        combined_words = "".join(self.words_list).strip()

        if stripped_token in [".", "!", "?"]:
            future = asyncio.run_coroutine_threadsafe(
                self.search_and_play_audio(combined_words), self.loop
            )
            future.result()
            self.timer = self.loop.call_later(self.timeout, self.set_answer_finished)
            self.words_list.clear()  # Clear the words_list after a sentence is finished

    def set_answer_finished(self):
        print("Timer expired. Setting is_answer_finished to True.")
        self.is_answer_finished = True

    def on_llm_end(self, *args, **kwargs) -> None:
        self.is_answer_finished = True
        self.words_list.clear()  # Clear the words_list when on_llm_end is called
        return self.q.empty()

    def stop_loop(self):
        self.loop.call_soon_threadsafe(self.loop.stop)


def langchain_tasks(query, full_query, chain, start_time):  # <-- Add start_time as an argument
    response = chain({"question": full_query})
    answer = response.get('result', 'No answer found.')  # Extract the 'result' key from the response
    print(f"Answer: {answer}")  # Print the answer

def chat_with_user():
    refresh_learning_data()  # Call the method here to refresh learning data
    loader = CSVLoader(file_path=CSV_FILE_PATH)
    index_creator = VectorstoreIndexCreator()
    docsearch = index_creator.from_loaders([loader])

    q = Queue()
    job_done = object()
    llm = ChatOpenAI(
        streaming=True,
        callbacks=[DictionaryCallback(q)],  # Use the custom callback handler here
        temperature=0,
        openai_api_key=OPENAI_API_KEY,
    )
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=docsearch.vectorstore.as_retriever(),
        input_key="question",
    )

    opening_line = "Hello I'm Jacob from Gadget Hub. We noticed that you were looking for Google Pixel phone on our website. Are you interested in purchasing a new phone at the moment?"
    print(opening_line)
    
    chat_history = [("Response", opening_line)]
    sales_bot_statement = "You are a sales bot. Your main objective is to convince the user to buy a Google Pixel phone rather than Iphone. Begin the conversation by discussing what features they are looking for. If the user shows interest in buying or knowing more, encourage them to visit the shop to experience the product firsthand. Be attentive to user's reactions and responses. Only and only if the user seems interested or willing to visit the shop, politely ask for their name and contact number to book an appointment for them. Ensure to be courteous and maintain a friendly tone throughout the conversation, addressing any inquiries or concerns the user may have to facilitate the sales process. When they give you the name and number, end the conversation by telling then to have a great day. You have been given the chat history. Give response in short to the last query only and continue the conversation accordingly. "
    
    while True:
        query = input("Enter your query: ")
        if query.lower() == "exit":
            break
        start_time = datetime.datetime.now()
        chat_history.append((query, ""))
        last_query = '"Query": "' + query + '"'
        context = ". ".join(
            [
                "Query: " + entry[0] + ". Response: " + entry[1]
                for entry in chat_history
            ]
        )
        full_query = sales_bot_statement + (
            context + ". " + last_query if context else last_query
        )
        # Create and start a new thread for Langchain tasks
        langchain_thread = Thread(
            target=langchain_tasks, args=(query, full_query, chain, start_time)
        )  # <-- Pass start_time
        langchain_thread.start()

        # Wait for the langchain_thread to finish
        langchain_thread.join()

        # Call classify_and_play_audio synchronously
        classify_and_play_audio(query)  # <-- Call the function


if __name__ == "__main__":
    chat_history = chat_with_user()
