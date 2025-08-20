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

    prompt = "Generate a DHCP log entry in the following format. Replace <hardware_address> with a realistic MAC address, <ip_address> with realistic IPv4 addresses, and <hostname> with a plausible hostname. Dates should be realistic and consistent across fields. Randomize counts and timestamps to make the log look authentic.\n\nFormat:\nLooking for hardware address <hardware_address>\n\n    last request   : <YYYY-MM-DD HH:MM:SS>\n    type           : dhcp\n    gateway        : direct\n    status         : found\n    ip             : <ip_address> (<hostname>)\n\n         server   count      most recent           first          IP address\n         ======  =======  =================  =================  ===============\n\n DISCOVER:    1       <count>  <MM/DD/YY HH:MM:SS>  <MM/DD/YY HH:MM:SS>  <ip_address>\n              2       <count>           <HH:MM:SS>           <HH:MM:SS>  <ip_address>\n\n OFFER:       1       <count>  <MM/DD/YY HH:MM:SS>  <MM/DD/YY HH:MM:SS>  <ip_address>\n              2       <count>           <HH:MM:SS>           <HH:MM:SS>  <ip_address>\n\n REQUEST:     1       <count>  <MM/DD/YY HH:MM:SS>  <MM/DD/YY HH:MM:SS>  <ip_address>\n              2       <count>  <MM/DD/YY HH:MM:SS>           <HH:MM:SS>  <ip_address>\n\n ACK:         1       <count>  <MM/DD/YY HH:MM:SS>  <MM/DD/YY HH:MM:SS>  <ip_address>\n              2       <count>  <MM/DD/YY HH:MM:SS>           <HH:MM:SS>  <ip_address>\n\n RELEASE:     1       <count>  <MM/DD/YY HH:MM:SS>  <MM/DD/YY HH:MM:SS>  <ip_address>"
    reply = chat_with_mistral(prompt)

    print("Prompt:", prompt)

    print("Mistral says:", reply)

    with open('testoutput.txt', 'w') as file:
        file.write(reply)
        file.write("\n")


