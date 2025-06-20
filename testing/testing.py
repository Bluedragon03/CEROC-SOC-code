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



# Example usage

if __name__ == "__main__":

    prompt = input("enter a prompt: ")

    reply = chat_with_mistral(prompt)

    print("Mistral says:", reply)

    with open('testoutput.txt', 'w') as file:
        file.write(reply)
        file.write("\n")


