import requests
import csv
import random

wallet_address = "PUT_HERE_SOMEONES_NODE" # Someones node with high throughput
node_url = f"https://{wallet_address}.us.gaianet.network/v1/chat/completions"

headers = {
    "accept": "application/json",
    "Content-Type": "application/json"
}

def get_random_word(words):
    return random.choice(words)

def get_words_list():
    words_list = []

    # Open and read the CSV file
    with open('random_words.csv', mode='r') as file:
        # Create a CSV reader object
        csv_reader = csv.reader(file)
        
        # Skip the header row
        next(csv_reader)
        
        # Loop through the rows in the CSV
        for row in csv_reader:
            # Add the word to the list
            words_list.append(row[0])

    return words_list
    
def extract_reply(response):
    if response and 'choices' in response:
        return response['choices'][0]['message']['content']
    return ""

def get_random_question(random_word):
    question = f'Generate next small and simple random question about {random_word}. Just plain question, nothing else. No your comments.'
    message = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant. You provide random different question."},
            {"role": "user", "content": question}
        ]
    }

    try:
        response = requests.post(node_url, json=message, headers=headers)
        response.raise_for_status()
        data = response.json()

        return extract_reply(data) 
    except requests.exceptions.RequestException as e:
        print(f"Failed to get response from API: {e}")
        return None
    
def get_question_templates():
    questions = []

    # Open and read the CSV file
    with open('question-templates.csv', mode='r') as file:
        # Create a CSV reader object
        csv_reader = csv.reader(file)
        
        # Skip the header row
        next(csv_reader)
        
        # Loop through the rows in the CSV
        for row in csv_reader:
            # Add the word to the list
            questions.append(row[0])

    return questions

def get_random_question_local(words, questions_templates):
    word = get_random_word(words)
    rnd_template = random.choice(questions_templates)
    random_question = rnd_template.replace("{placeholder-for-noun}", word)

    return random_question

if __name__ == '__main__':
    words = get_words_list()
    templates = get_question_templates()

    print(get_random_question_local(words, templates))
