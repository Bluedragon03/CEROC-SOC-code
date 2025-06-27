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

    prompt = "Generate exactly 50 lines of realistic DNS log entries. Each line should resemble output from a DNS server log, including a timestamp, client IP address, query type, domain name, and response code. Do not include any explanation, headers, or comments—only the 50 lines of raw log data."

    print("getting response from mistral")
    
    reply = chat_with_mistral(prompt)

    print("printing reply to outputlog.txt")

    with open('outputlog.txt', 'w') as file:

        file.write(reply)

        file.write("\n")
