import requests


def chat_with_mistral(prompt):

    url = "http://localhost:11434/api/generate"

    payload = {

        "model": "mistral",

        "prompt": prompt,

        "stream": False  # Set to True if you want streamed responses

    }

    response = requests.post(url, json=payload)

    response.raise_for_status()  # Raise an exception for HTTP errors

    result = response.json()

    return result['response']


if __name__ == "__main__":

    prompt = "generate a dns log that contains signs of a ddos attack. the log should contain atleast 50 lines of data. do not respond with anything except for the data in the log."

    print("getting response from mistral")
    
    reply = chat_with_mistral(prompt)

    print("printing reply to outputlog.txt")

    with open('outputlog.txt', 'w') as file:

        file.write(reply)

        file.write("\n")
