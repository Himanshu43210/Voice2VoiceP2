from datetime import datetime
import faiss
from sklearn.feature_extraction.text import TfidfVectorizer

# Read the possible responses from a .txt file
with open("needToTest.txt", "r") as file:
    given_responses = [line.strip() for line in file.readlines()]

vectorizer = TfidfVectorizer()
response_matrix = vectorizer.fit_transform(given_responses).toarray()

# Define the dimensionality of the vectors
d = response_matrix.shape[1]

# Create a FAISS index for the given responses
index = faiss.IndexFlatL2(d)
index.add(response_matrix.astype("float32"))


def find_most_similar(input_sentence):
    vectorized_sentence = (
        vectorizer.transform([input_sentence]).toarray().astype("float32")
    )

    # Search the index for the closest vector
    distances, indices = index.search(vectorized_sentence, k=1)

    # Convert the L2 distance to a similarity score between 0 and 1
    similarity_score = 1 / (1 + distances[0][0])

    return given_responses[indices[0][0]], similarity_score


input_sentences = [
    "Absolutely, we have numerous success stories to share! Countless clients have reached their career aspirations thanks to our team. Check out their testimonials on our site.",
    "Indeed, our portfolio includes many success stories! Through our assistance, numerous clients have realized their professional dreams. Their accounts are available for reading on our webpage.",
    "Of course, we're proud to share the success stories of our clients! With our team's guidance, many have achieved remarkable career milestones. Visit our website to delve into their journeys.",
    "We certainly do have success stories to offer! Our team has been pivotal in helping several clients attain their career objectives. Their tales are prominently featured on our online platform.",
    "Without a doubt, success stories are part of our brand! Many have climbed their career ladders with our team's support. Their narratives are chronicled on our website for your perusal.",
]

for input_sentence in input_sentences:
    start_time = datetime.now()

    response, similarity_score = find_most_similar(input_sentence)

    end_time = datetime.now()
    time_taken = (end_time - start_time).total_seconds()  # Time taken in seconds

    print("Input Text:", input_sentence)
    print("Output Text:", response)
    print(f"Similarity Score: {similarity_score:.4f}")
    print(f"Time Taken: {time_taken:.4f} seconds")
    print("---------------------------------------------------------")
