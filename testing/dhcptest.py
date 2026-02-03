import requests

import random

import re

from datetime import datetime, timedelta



def process_output(reply, log_string, section_label, global_id, base_time):

    log_string += f"\n\n{section_label:<15}"

    lines = reply.strip().splitlines()

    current_id = global_id

    first_line = True

    

    # Each packet in a section happens slightly after the base_time

    # We increment by milliseconds to keep it realistic

    current_time = base_time



    # Updated Regex to extract just the IP and any other data Mistral provides

    # Since we are generating the Time/ID/Count ourselves now

    log_pattern = re.compile(r"(\d{1,3}(?:\.\d{1,3}){3})")



    for line in lines:

        match = log_pattern.search(line)

        if match:

            ip = match.group(1)

            

            # 1. Generate realistic timestamps

            # 'first' is when it started, 'most recent' is slightly later

            first_dt = current_time

            recent_dt = current_time + timedelta(seconds=random.randint(1, 3))

            

            d1, t1 = recent_dt.strftime("%Y-%m-%d"), recent_dt.strftime("%H:%M:%S")

            d2, t2 = first_dt.strftime("%Y-%m-%d"), first_dt.strftime("%H:%M:%S")

            

            # 2. Format the row

            indent = "" if first_line else " " * 15

            log_string += f"{indent}{current_id:>2} {1:>7}   {d1} {t1}   {d2} {t2}   {ip}\n"

            

            # 3. Increment for the next row in this section

            current_id += 1

            current_time += timedelta(seconds=random.randint(1, 2))

            first_line = False

                

    return log_string, current_id, current_time



# ... (chat_with_mistral remains the same)
def chat_with_mistral(prompt):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.1}
    }
    try:
        return requests.post(url, json=payload).json()['response']
    except:
        return ""



if __name__ == "__main__":

    session_ip = "192.168.1.105"

    # Start the log at a specific time

    log_clock = datetime(2026, 2, 3, 14, 0, 0)

    

    log_string = f"Looking for hardware address 00:11:22:33:44:55\n\n"

    log_string += f"    last request   : {log_clock.strftime('%Y-%m-%d %H:%M:%S')}\n"

    log_string += f"    type           : dhcp\n    ip             : {session_ip}"

    log_string += "\n\n                ID   count      most recent               first                 IP address"

    log_string += "\n               ====  =======  =====================  =====================  ==============="



    global_id = 1

    # Define the sequence: (Section Name, Rows to Generate)

    # This ensures a perfect DORA sequence

    sequence = [("DISCOVER", 1), ("OFFER", 1), ("REQUEST", 1), ("ACK", 1)]



    for name, rows in sequence:

        # Prompt Mistral just for the IPs/Scenario data

        prompt = f"Generate {rows} rows of DHCP {name} data for IP {session_ip}. Only output the IP address."

        reply = chat_with_mistral(prompt)

        

        # Pass the log_clock into the processor so it knows when the last event ended

        log_string, global_id, log_clock = process_output(reply, log_string, f"{name}:", global_id, log_clock)

        

        # Add a small delay between D-O-R-A stages

        log_clock += timedelta(milliseconds=random.randint(200, 800))



    print(log_string)
