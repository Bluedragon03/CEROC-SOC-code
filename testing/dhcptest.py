import requests

import random

import re

from datetime import datetime, timedelta



def process_output(reply, log_string, section_label, global_id, base_time, is_attack=False):

    log_string += f"\n\n{section_label:<15}"

    current_id = global_id

    current_time = base_time

    first_line = True



    # Regex to find any IPv4 address in the AI's response

    ip_pattern = re.compile(r"(\d{1,3}(?:\.\d{1,3}){3})")

    found_ips = ip_pattern.findall(reply)



    for ip in found_ips:

        # 1. Timing Jitter

        # Attacks happen much faster (milliseconds) than normal traffic

        ms_delay = random.randint(10, 100) if is_attack else random.randint(500, 2000)

        first_dt = current_time

        recent_dt = current_time + timedelta(milliseconds=ms_delay)

        

        d1, t1 = recent_dt.strftime("%Y-%m-%d"), recent_dt.strftime("%H:%M:%S")

        d2, t2 = first_dt.strftime("%Y-%m-%d"), first_dt.strftime("%H:%M:%S")

        

        # 2. Formatting

        indent = "" if first_line else " " * 15

        log_string += f"{indent}{current_id:>2} {1:>7}   {d1} {t1}   {d2} {t2}   {ip}\n"

        

        # 3. Advancement

        current_id += 1

        # In starvation, packets hit the server almost simultaneously

        gap = random.randint(1, 5) if is_attack else random.randint(1, 3)

        current_time += timedelta(milliseconds=gap if is_attack else gap * 1000)

        first_line = False

                

    return log_string, current_id, current_time



def chat_with_mistral(prompt):

    url = "http://localhost:11434/api/generate"

    payload = {"model": "mistral", "prompt": prompt, "stream": False, "options": {"temperature": 0.15}}

    try:

        return requests.post(url, json=payload).json()['response']

    except: return "192.168.1.105" # Fallback IP



if __name__ == "__main__":

    # MODES: "normal", "starvation", "spoofing"

    
    logtype = int(input("Please select an attack:\n1. Normal\n2. DHCP Starvation\n3. DHCP Spoofing\n"))

    if logtype == 1:

        SIMULATION_MODE = "normal"

    elif logtype == 2:

        SIMULATION_MODE = "starvation"

    elif logtype == 3:

        SIMULATION_MODE = "spoofing"

    else:

        print("Not an option")

        exit()
    
    session_ip = "192.168.1.105"

    log_clock = datetime(2026, 2, 3, 14, 0, 0)

    global_id = 1

    log_string = f"DHCP SERVER LOG - MODE: {SIMULATION_MODE.upper()}\n"

    log_string += f"Looking for hardware address 00:11:22:33:44:55\n\n"

    log_string += f"    last request   : {log_clock.strftime('%Y-%m-%d %H:%M:%S')}\n"

    log_string += f"    type           : dhcp\n"

    log_string += "                ID   count      most recent               first                 IP address\n"

    log_string += "               ====  =======  =====================  =====================  ==============="

    # Define Attack/Normal Sequences

    if SIMULATION_MODE == "starvation":
        sequence = [("DISCOVER", 20)]
        prompt_extra = "Generate 20 unique random IPv4 addresses. Output only the IPs."
    elif SIMULATION_MODE == "spoofing":
        sequence = [("DISCOVER", 1), ("OFFER", 2), ("REQUEST", 1), ("ACK", 1)]
        prompt_extra = f"Provide exactly the IPs requested. Row 1: {session_ip}, Row 2: 10.0.0.66."
    else:
        # NORMAL MODE: Only 1 row per stage!
        sequence = [("DISCOVER", 1), ("OFFER", 1), ("REQUEST", 1), ("ACK", 1)]
        prompt_extra = f"Output ONLY the IP address: {session_ip}. Do not provide any other IPs."

    for name, rows in sequence:

        is_atk = (SIMULATION_MODE == "starvation" and name == "DISCOVER") or (SIMULATION_MODE == "spoofing" and name == "OFFER")

        prompt = f"Task: {name} log data. {prompt_extra} Output only raw IP addresses."

        reply = chat_with_mistral(prompt)

        log_string, global_id, log_clock = process_output(reply, log_string, f"{name}:", global_id, log_clock, is_atk)

        log_clock += timedelta(milliseconds=200)

    print(log_string)
