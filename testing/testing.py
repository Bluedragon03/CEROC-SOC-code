import requests

def process_output(reply, log_string):

    try:

        print("Processing Output")

        log_lines = reply.splitlines()

        line_count = 0

        for line in log_lines:

            if line_count > 0:

                line_list = line.split()

                if len(line_list) > 1 and len(line_list) != 6:

                    new_line = "             " + line_list[0] + "       " + line_list[1] + "                  " + line_list[2] + "             " + line_list[3] + "  " + line_list[4]
                
                    log_string = log_string + new_line + "\n"

                    line_count = line_count + 1
                else:

                    new_line = "             " + line_list[0] + "       " + line_list[1] + "                  " + line_list[3] + "             " + line_list[5] + "  " + line_list[6]
                    
                    log_string = log_string + new_line + "\n"

                    line_count = line_count + 1

            else:

                line_list = line.split()

                if len(line_list) > 1:

                    new_line = " " + line_list[0] + "       " + line_list[1] + "       " + line_list[2] + " " + line_list[3] + "  " + line_list[4] + " " + line_list[5] + "  " + line_list[6]

                    log_string = log_string + new_line + "\n"

                    line_count = line_count + 1

    except:
        print(reply)

    return log_string


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

    prompt1 = "Generate the DHCP log header in the following format. Replace <hardware_address> with a realistic MAC address, <ip_address> with a realistic IPv4 address, and <hostname> with a plausible hostname. The date should be realistic.\n\nFormat:\nLooking for hardware address <hardware_address>\n\n    last request   : <YYYY-MM-DD HH:MM:SS>\n    type           : dhcp\n    gateway        : direct\n    status         : found\n    ip             : <ip_address> (<hostname>)"
    
    prompt2 = "Generate the DISCOVER section of the DHCP log in the following format. Replace <count> with a number, <ip_address> with realistic IPv4 addresses, and times with realistic values. Strictly replicate the spacing and newlines in the given format. Do not output anything else.\n\nFormat:\n 1       <count>  <MM/DD/YY HH:MM:SS>  <MM/DD/YY HH:MM:SS>  <ip_address>\n              2       <count>           <HH:MM:SS>           <HH:MM:SS>  <ip_address>"
    
    prompt3 = "Generate the OFFER section of the DHCP log in the following format. Replace <count> with a number, <ip_address> with realistic IPv4 addresses, and times with realistic values. Strictly replicate the spacing and newlines in the given format. Do not output anything else. Your response should not include the 'OFFER:' part of the format.\n\nFormat:\n 1       <count>  <MM/DD/YY HH:MM:SS>  <MM/DD/YY HH:MM:SS>  <ip_address>\n              2       <count>           <HH:MM:SS>           <HH:MM:SS>  <ip_address>"
    
    prompt4 = "Generate the REQUEST section of the DHCP log in the following format. Replace <count> with a number, <ip_address> with realistic IPv4 addresses, and times with realistic values.\n\nFormat:\n REQUEST:     1       <count>  <MM/DD/YY HH:MM:SS>  <MM/DD/YY HH:MM:SS>  <ip_address>\n              2       <count>  <MM/DD/YY HH:MM:SS>           <HH:MM:SS>  <ip_address>"
    
    prompt5 = "Generate the ACK section of the DHCP log in the following format. Replace <count> with a number, <ip_address> with realistic IPv4 addresses, and times with realistic values.\n\nFormat:\n ACK:         1       <count>  <MM/DD/YY HH:MM:SS>  <MM/DD/YY HH:MM:SS>  <ip_address>\n              2       <count>  <MM/DD/YY HH:MM:SS>           <HH:MM:SS>  <ip_address>"
    
    prompt6 = "Generate the RELEASE section of the DHCP log in the following format. Replace <count> with a number, <ip_address> with realistic IPv4 addresses, and times with realistic values.\n\nFormat:\n RELEASE:     1       <count>  <MM/DD/YY HH:MM:SS>  <MM/DD/YY HH:MM:SS>  <ip_address>"

    log_string = ""
    
    print("Generating Header")
    
    reply = chat_with_mistral(prompt1)

    log_string = log_string + reply

    log_string = log_string + "\n\n             server   count      most recent           first          IP address"
    log_string = log_string + "\n             ======  =======  =================  =================  ===============  "

    print("Generating Discover")

    reply = chat_with_mistral(prompt2 + "\nThe previous sections of the log are the following: \n" + log_string)

    log_string = log_string + "\n\n" + "DISCOVER:   "

    log_string = process_output(reply, log_string)

    print("Generating Offer")
    
    reply = chat_with_mistral(prompt3 + "\nThe previous sections of the log are the following: \n" + log_string)

    log_string = log_string + "\n\n" + "OFFER:      "

    log_string = process_output(reply, log_string)

    print("Mistral says:", log_string)

    with open('testoutput.txt', 'w') as file:
        file.write(log_string)
        file.write("\n")


