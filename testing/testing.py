import requests

def process_output(reply, log_string):
    # Split the AI reply into lines
    lines = reply.strip().splitlines()
    
    for line in lines:
        parts = line.split()
        # Ensure we have exactly 7 parts (ID, Count, Date1, Time1, Date2, Time2, IP)
        if len(parts) == 7:
            # Re-format with clean tab-like spacing
            formatted = f"{parts[0]:>14} {parts[1]:>7}   {parts[2]} {parts[3]}   {parts[4]} {parts[5]}   {parts[6]}"
            log_string += formatted + "\n"
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

    prompt1 = "Role: You are a DHCP log generator. Task: Generate a DHCP log header. Values: Use MAC 00:11:22:33:44:55, IP 192.168.1.100, Hostname workstation-01, and a realistic recent date. Constraint: Output only the text below. No conversational filler.\n\nFormat: Looking for hardware address <hardware_address>\n\nlast request   : <YYYY-MM-DD HH:MM:SS>\ntype           : dhcp\ngateway        : direct\nstatus         : found\nip             : <ip_address> (<hostname>)"
    
    prompt2 = "Role: You are a DHCP log generator. Task: Generate the DISCOVER section. Requirements:\n\nUse exactly 7 columns: [ID] [Count] [Start_Date] [Start_Time] [End_Date] [End_Time] [IP].\n\nUse YYYY-MM-DD for dates and HH:MM:SS for times.\n\nCrucial: Do not include labels like 'DISCOVER:' or any headers.\n\nDo not include markdown code blocks or conversational text.\n\nFormat Template: 1 1 2026-01-29 12:00:01 2026-01-29 12:00:05 192.168.1.101 2 1 2026-01-29 12:00:02 2026-01-29 12:00:06 192.168.1.102"
    
    prompt3 = "Role: You are a DHCP log generator. Task: Generate the OFFER section. Requirements:\n\nUse exactly 7 columns: [ID] [Count] [Start_Date] [Start_Time] [End_Date] [End_Time] [IP].\n\nUse YYYY-MM-DD for dates and HH:MM:SS for times.\n\nCrucial: Do not include labels like 'OFFER:' or any headers.\n\nDo not include markdown code blocks or conversational text.\n\nFormat Template: 1 1 2026-01-29 12:00:01 2026-01-29 12:00:05 192.168.1.101 2 1 2026-01-29 12:00:02 2026-01-29 12:00:06 192.168.1.102"
    
    prompt4 = "Role: You are a DHCP log generator. Task: Generate the REQUEST section. Requirements:\n\nUse exactly 7 columns: [ID] [Count] [Start_Date] [Start_Time] [End_Date] [End_Time] [IP].\n\nUse YYYY-MM-DD for dates and HH:MM:SS for times.\n\nCrucial: Do not include labels like 'REQUEST:' or any headers.\n\nDo not include markdown code blocks or conversational text.\n\nFormat Template: 1 1 2026-01-29 12:00:01 2026-01-29 12:00:05 192.168.1.101 2 1 2026-01-29 12:00:02 2026-01-29 12:00:06 192.168.1.102"
    
    prompt5 = "Role: You are a DHCP log generator. Task: Generate the ACK section. Requirements:\n\nUse exactly 7 columns: [ID] [Count] [Start_Date] [Start_Time] [End_Date] [End_Time] [IP].\n\nUse YYYY-MM-DD for dates and HH:MM:SS for times.\n\nCrucial: Do not include labels like 'ACK:' or any headers.\n\nDo not include markdown code blocks or conversational text.\n\nFormat Template: 1 1 2026-01-29 12:00:01 2026-01-29 12:00:05 192.168.1.101 2 1 2026-01-29 12:00:02 2026-01-29 12:00:06 192.168.1.102"
    
    prompt6 = "Role: You are a DHCP log generator. Task: Generate the RELEASE section. Requirements:\n\nUse exactly 7 columns: [ID] [Count] [Start_Date] [Start_Time] [End_Date] [End_Time] [IP].\n\nUse YYYY-MM-DD for dates and HH:MM:SS for times.\n\nCrucial: Do not include labels like 'RELEASE:' or any headers.\n\nDo not include markdown code blocks or conversational text.\n\nFormat Template: 1 1 2026-01-29 12:00:01 2026-01-29 12:00:05 192.168.1.101 2 1 2026-01-29 12:00:02 2026-01-29 12:00:06 192.168.1.102"

    log_string = ""
    
    print("Generating Header")
    
    reply = chat_with_mistral(prompt1)

    log_string = log_string + reply

    log_string = log_string + "\n\n             server   count      most recent           first          IP address"
    log_string = log_string + "\n             ======  =======  =================  =================  ===============  "

    print("Generating Discover")

    reply = chat_with_mistral(prompt2)# + "\nThe previous sections of the log are the following: \n" + log_string)

    log_string = log_string + "\n\n" + "DISCOVER:"

    log_string = process_output(reply, log_string)

    print("Generating Offer")
    
    reply = chat_with_mistral(prompt3)# + "\nThe previous sections of the log are the following: \n" + log_string)

    log_string = log_string + "\n\n" + "OFFER:"

    log_string = process_output(reply, log_string)

    print("Generating Request")

    reply = chat_with_mistral(prompt4)# + "\nThe previous sections of the log are the following: \n" + log_string)

    log_string = log_string + "\n\n" + "REQUEST:"

    log_string = process_output(reply, log_string)

    print("Generating Ack")

    reply = chat_with_mistral(prompt5)# + "\nThe previous sections of the log are the following: \n" + log_string)
    
    log_string = log_string + "\n\n" + "ACK:"

    log_string = process_output(reply, log_string)

    print("Generating Release")

    reply = chat_with_mistral(prompt6)# + "\nThe previous sections of the log are the following: \n" + log_string)

    log_string = log_string + "\n\n" + "RELEASE:"

    log_string = process_output(reply, log_string)

    print(log_string)

    with open('testoutput.txt', 'w') as file:
        file.write(log_string)
        file.write("\n")


