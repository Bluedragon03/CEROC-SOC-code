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


def chat_with_codellama(prompt):

    url = "http://localhost:11434/api/generate"

    payload = {

        "model": "codellama",

        "prompt": prompt,

        "stream": False  # Set to True if you want streamed responses

    }

    response = requests.post(url, json=payload)

    response.raise_for_status()  # Raise an exception for HTTP errors

    result = response.json()

    return result['response']


# Example usage

if __name__ == "__main__":

    prompt = "give me an example log file showing a ddos attack"

    print("getting mistral response\n")
    
    reply1 = chat_with_mistral(prompt)

    print("getting codellama response\n")

    reply2 = chat_with_codellama(prompt)

    print("printing mistral response to file\n")
    
    with open('mistrallog.txt', 'w') as file:
        file.write(reply1)
        file.write("\n")

    print("printing codellama response to file\n")
    
    with open('codellamalog.txt', 'w') as file:
        file.write(reply2)
        file.write("\n")


