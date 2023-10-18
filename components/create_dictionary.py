# text = """
# Great! I can definitely help you with that. What specific features are you looking for in a phone?
# The Google Pixel is known for its exceptional camera quality. It has a high-resolution camera that captures stunning photos with great detail and vibrant colors. You'll be able to take professional-looking photos with ease. Would you like to visit our showroom to experience the camera firsthand? Can I have your name and contact number to schedule an appointment for you to visit our shop?
# Great! I'd be happy to help you find the perfect phone. Do you have any specific features in mind that you're looking for in a phone, or are you open to suggestions?
# The Google Pixel is known for its exceptional camera quality. It has a high-resolution camera with advanced features like Night Sight and Portrait Mode. You'll be able to capture stunning photos and videos with great clarity and detail. Would you like to visit our showroom to experience the camera firsthand? Can I have your name and contact number to schedule an appointment for you to visit our shop?
# Thank you, John. I've scheduled your personal demo for this Saturday. If you have any questions, please don't hesitate to contact us. Have a great day!
# Great! I'm glad to hear that you're interested in purchasing a new phone. The Google Pixel is an excellent choice. Can you please let me know what specific features you are looking for in a phone? This will help me provide you with the best recommendations and information.
# I understand that you are mainly concerned about the quality of the camera. The Google Pixel phones are known for their exceptional camera capabilities. They have advanced camera features like Night Sight, which allows you to capture stunning low-light photos, and Portrait Mode, which creates professional-looking photos with a blurred background effect. If you're interested, I would recommend visiting our shop to experience the Google Pixel's camera firsthand. Would you like to schedule an appointment?
# Great choice! We'd be happy to give you a hands-on demo. Please let me know your name and contact number so that I can book an appointment for you.
# Thank you, John. I've scheduled your personal demo for this Saturday. If you have any questions, please don't hesitate to contact us. Have a great day!
# """

# # Splitting the text into sentences
# import re
# sentences = re.split(r'[.!?]', text)

# # Cleaning and creating the dictionary
# phrases_dict = {}
# for sentence in sentences:
#     cleaned_sentence = sentence.strip()
#     if cleaned_sentence:  # Checking if the sentence is not empty
#         filename = re.sub(r'[^a-zA-Z0-9]', '', cleaned_sentence) + ".wav"
#         phrases_dict[cleaned_sentence + "." if not cleaned_sentence.endswith(("!", "?")) else cleaned_sentence] = filename

# print(phrases_dict)

# {
#     'Great.': 'Great.wav',
#     'I can definitely help you with that.': 'Icandefinitelyhelpyouwiththat.wav',
#     'What specific features are you looking for in a phone.': 'Whatspecificfeaturesareyoulookingforinaphone.wav',
#     'The Google Pixel is known for its exceptional camera quality.': 'TheGooglePixelisknownforitsexceptionalcameraquality.wav',
#     'It has a high-resolution camera that captures stunning photos with great detail and vibrant colors.': 'Ithasahighresolutioncamerathatcapturesstunningphotoswithgreatdetailandvibrantcolors.wav',
#     "You'll be able to take professional-looking photos with ease.": 'Youllbeabletotakeprofessionallookingphotoswithease.wav',
#     'Would you like to visit our showroom to experience the camera firsthand.': 'Wouldyouliketovisitourshowroomtoexperiencethecamerafirsthand.wav',
#     'Can I have your name and contact number to schedule an appointment for you to visit our shop.': 'CanIhaveyournameandcontactnumbertoscheduleanappointmentforyoutovisitourshop.wav',
#     "I'd be happy to help you find the perfect phone.": 'Idbehappytohelpyoufindtheperfectphone.wav',
#     "Do you have any specific features in mind that you're looking for in a phone, or are you open to suggestions.": 'Doyouhaveanyspecificfeaturesinmindthatyourelookingforinaphoneorareyouopentosuggestions.wav',
#     'It has a high-resolution camera with advanced features like Night Sight and Portrait Mode.': 'IthasahighresolutioncamerawithadvancedfeatureslikeNightSightandPortraitMode.wav',
#     "You'll be able to capture stunning photos and videos with great clarity and detail.": 'Youllbeabletocapturestunningphotosandvideoswithgreatclarityanddetail.wav',
#     'Thank you, John.': 'ThankyouJohn.wav',
#     "I've scheduled your personal demo for this Saturday.": 'IvescheduledyourpersonaldemoforthisSaturday.wav',
#     "If you have any questions, please don't hesitate to contact us.": 'Ifyouhaveanyquestionspleasedonthesitatetocontactus.wav',
#     'Have a great day.': 'Haveagreatday.wav',
#     "I'm glad to hear that you're interested in purchasing a new phone.": 'Imgladtohearthatyoureinterestedinpurchasinganewphone.wav',
#     'The Google Pixel is an excellent choice.': 'TheGooglePixelisanexcellentchoice.wav',
#     'Can you please let me know what specific features you are looking for in a phone.': 'Canyoupleaseletmeknowwhatspecificfeaturesyouarelookingforinaphone.wav',
#     'This will help me provide you with the best recommendations and information.': 'Thiswillhelpmeprovideyouwiththebestrecommendationsandinformation.wav',
#     'I understand that you are mainly concerned about the quality of the camera.': 'Iunderstandthatyouaremainlyconcernedaboutthequalityofthecamera.wav',
#     'The Google Pixel phones are known for their exceptional camera capabilities.': 'TheGooglePixelphonesareknownfortheirexceptionalcameracapabilities.wav',
#     'They have advanced camera features like Night Sight, which allows you to capture stunning low-light photos, and Portrait Mode, which creates professional-looking photos with a blurred background effect.': 'TheyhaveadvancedcamerafeatureslikeNightSightwhichallowsyoutocapturestunninglowlightphotosandPortraitModewhichcreatesprofessionallookingphotoswithablurredbackgroundeffect.wav',
#     "If you're interested, I would recommend visiting our shop to experience the Google Pixel's camera firsthand.": 'IfyoureinterestedIwouldrecommendvisitingourshoptoexperiencetheGooglePixelscamerafirsthand.wav',
#     'Would you like to schedule an appointment.': 'Wouldyouliketoscheduleanappointment.wav',
#     'Great choice.': 'Greatchoice.wav',
#     "We'd be happy to give you a hands-on demo.": 'Wedbehappytogiveyouahandsondemo.wav',
#     'Please let me know your name and contact number so that I can book an appointment for you.': 'PleaseletmeknowyournameandcontactnumbersothatIcanbookanappointmentforyou.wav'
# }

text = """
I'd be happy to help. Do you have a specific feature in mind, or are you open to suggestions?
I understand your concern about the camera quality. The Google Pixel phones are known for their exceptional camera capabilities. They have advanced camera features like Night Sight, which allows you to capture stunning low-light photos, and Portrait Mode, which creates professional-looking bokeh effects. Additionally, the Google Pixel phones have excellent image processing software that enhances the overall image quality. If you're interested, I would recommend visiting our shop to experience the camera performance firsthand. Would you like to schedule an appointment?
Great! We'd love to show you the Google Pixel's camera quality in person at our showroom. Please let me know your name and contact number so that I can book an appointment for you.
"""

# Splitting the text into sentences
import re
sentences = re.split(r'(?<=[.!?])', text)

# Cleaning and creating the dictionary
phrases_dict = {}
for sentence in sentences:
    cleaned_sentence = sentence.strip()
    if cleaned_sentence:  # Checking if the sentence is not empty
        filename = re.sub(r'[^a-zA-Z0-9]', '', cleaned_sentence) + ".wav"
        phrases_dict[cleaned_sentence] = filename

# Printing the dictionary with each key-value pair on a new line
for key, value in phrases_dict.items():
    print(f"'{key}': '{value}',")
# {
#     'Great!': 'Great.wav',
#     'I can definitely help you with that.': 'Icandefinitelyhelpyouwiththat.wav',
#     'What specific features are you looking for in a phone?': 'Whatspecificfeaturesareyoulookingforinaphone.wav',
#     'The Google Pixel is known for its exceptional camera quality.': 'TheGooglePixelisknownforitsexceptionalcameraquality.wav',
#     'It has a high-resolution camera that captures stunning photos with great detail and vibrant colors.': 'Ithasahighresolutioncamerathatcapturesstunningphotoswithgreatdetailandvibrantcolors.wav',
#     "You 'll be able to take professional-looking photos with ease.": 'Youllbeabletotakeprofessionallookingphotoswithease.wav',
#     'Would you like to visit our showroom to experience the camera firsthand?': 'Wouldyouliketovisitourshowroomtoexperiencethecamerafirsthand.wav',
#     'Can I have your name and contact number to schedule an appointment for you to visit our shop?': 'CanIhaveyournameandcontactnumbertoscheduleanappointmentforyoutovisitourshop.wav',
#     "I 'd be happy to help you find the perfect phone.": 'Idbehappytohelpyoufindtheperfectphone.wav',
#     "Do you have any specific features in mind that you 're looking for in a phone, or are you open to suggestions?": 'Doyouhaveanyspecificfeaturesinmindthatyourelookingforinaphoneorareyouopentosuggestions.wav',
#     'It has a high-resolution camera with advanced features like Night Sight and Portrait Mode.': 'IthasahighresolutioncamerawithadvancedfeatureslikeNightSightandPortraitMode.wav', 
#     "You 'll be able to capture stunning photos and videos with great clarity and detail.": 'Youllbeabletocapturestunningphotosandvideoswithgreatclarityanddetail.wav',
#     'Thank you, John.': 'ThankyouJohn.wav',
#     "I 've scheduled your personal demo for this Saturday.": 'IvescheduledyourpersonaldemoforthisSaturday.wav',
#     "If you have any questions, please don 't hesitate to contact us.": 'Ifyouhaveanyquestionspleasedonthesitatetocontactus.wav',
#     'Have a great day!': 'Haveagreatday.wav',
#     "I 'm glad to hear that you're interested in purchasing a new phone.": 'Imgladtohearthatyoureinterestedinpurchasinganewphone.wav',
#     'The Google Pixel is an excellent choice.': 'TheGooglePixelisanexcellentchoice.wav',
#     'Can you please let me know what specific features you are looking for in a phone?': 'Canyoupleaseletmeknowwhatspecificfeaturesyouarelookingforinaphone.wav',
#     'This will help me provide you with the best recommendations and information.': 'Thiswillhelpmeprovideyouwiththebestrecommendationsandinformation.wav',
#     'I understand that you are mainly concerned about the quality of the camera.': 'Iunderstandthatyouaremainlyconcernedaboutthequalityofthecamera.wav',
#     'The Google Pixel phones are known for their exceptional camera capabilities.': 'TheGooglePixelphonesareknownfortheirexceptionalcameracapabilities.wav',
#     'They have advanced camera features like Night Sight, which allows you to capture stunning low-light photos, and Portrait Mode, which creates professional-looking photos with a blurred background effect.': 'TheyhaveadvancedcamerafeatureslikeNightSightwhichallowsyoutocapturestunninglowlightphotosandPortraitModewhichcreatesprofessionallookingphotoswithablurredbackgroundeffect.wav',
#     "If you 're interested, I would recommend visiting our shop to experience the Google Pixel's camera firsthand.": 'IfyoureinterestedIwouldrecommendvisitingourshoptoexperiencetheGooglePixelscamerafirsthand.wav',
#     'Would you like to schedule an appointment?': 'Wouldyouliketoscheduleanappointment.wav',
#     'Great choice!': 'Greatchoice.wav',
#     "We 'd be happy to give you a hands-on demo.": 'Wedbehappytogiveyouahandsondemo.wav',
#     'Please let me know your name and contact number so that I can book an appointment for you.': 'PleaseletmeknowyournameandcontactnumbersothatIcanbookanappointmentforyou.wav', 
# }
