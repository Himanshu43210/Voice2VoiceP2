import openai
import os
import csv
import openai

# OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
OPENAI_API_KEY = "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"

openai.api_key = OPENAI_API_KEY  # Set the API key explicitly

def get_conversation_points(scenario):
    # Construct the context prompt with more detailing
    context_prompt = f"Provide a detailed and elaborate conversation between a {scenario} dealer and a potential client, discussing various options, prices, and preferences."
    context_response = get_chatgpt_response(context_prompt)
    
    return {
        "context": context_response
    }

def get_chatgpt_response(prompt):
    try:
        response = openai.Completion.create(
            engine="davinci-instruct-beta",
            prompt=prompt,
            temperature=0.6,
            max_tokens=300  # Increased max tokens
        )
        return response.choices[0].text.strip()
    except openai.error.OpenAIError as e:
        return f"Error: {e}"

def write_to_csv(conversation_points):
    filename = "conversation_points.csv"
    fields = ["Context", "Query", "Response"]
    
    # Writing to csv file
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        
        # Write the header
        csvwriter.writerow(fields)
        
        # Write the data
        conversation_history = ""
        context_lines = conversation_points["context"].split('\n')
        for i, line in enumerate(context_lines):
            if line.strip():  # Check if line is not empty
                speaker = "Dealer" if i % 2 == 0 else "Client"
                conversation_history += f"{speaker}: {line.strip()}\n"
                if speaker == "Dealer":
                    user_prompt = f"Given the detailed context: '{conversation_history.strip()}', provide a suitable and detailed reply from a potential client discussing preferences, queries, or concerns."
                    user_response = get_chatgpt_response(user_prompt)
                    csvwriter.writerow([conversation_history.strip(), line.strip(), user_response])
                    conversation_history += f"Client: {user_response}\n"

if __name__ == "__main__":
    scenario = input("Enter the scenario: ")  # Get scenario from user input
    conversation_points = get_conversation_points(scenario)
    write_to_csv(conversation_points)
