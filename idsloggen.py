import requests
import re
import random
import time
import json
from datetime import datetime, timedelta

VECTOR_URL = "http://vector:8687"

domain_ip_map = {
        "google.com": "8.8.8.8",
        "zoom.us": "170.114.52.2",
        "teams.microsoft.com": "52.123.129.14",
        "outlook.com": "52.101.40.1",
        "gmail.com": "74.125.136.18",
        "linkedin.com": "150.171.22.12",
        "github.com": "140.82.112.3",
        "stackoverflow.com": "172.64.155.249",
        "youtube.com": "142.251.15.93",
        "cnn.com": "151.101.195.5",
        "nytimes.com": "151.101.1.164",
        "bbc.com": "151.101.64.81"
        }

def send_dns_traffic(log_string):
    proto_list = ["TCP", "UDP"]
    country_list = ["China", "Netherlands", "United States", "Vietnam", "Russia"]
    country_code_list = ["CN", "NL", "US", "VN", "RU"]
    
    for line in log_string.splitlines():
        line_parts = line.split()
        #print("timestamp: ", line_parts[0])
        #print("source ip: ", line_parts[1])
        #print("record type: ", line_parts[2])
        #print("domain: ", line_parts[3])
        #print("resolved ip: ", line_parts[4])
        #print("status code: ", line_parts[5])
        #print("type of attack: ", line_parts[6])
        
        src_country = random.choice(country_list)
        index = 0
        for country in country_list:
            if country == src_country:
                src_country_code = country_code_list[index]
            index = index + 1

        event = {
                "timestamp": line_parts[0],
                "event_type": "alert",
                "src_ip": line_parts[1],
                "src_port": 53,
                "dest_ip": line_parts[4],
                "dest_port": 53,
                "proto": random.choice(proto_list),

                #Heat Map Fields
                "src_country": src_country,
                "src_country_code": src_country_code,

                "alert": {
                    "action": "allowed",
                    "gid": 1,
                    "signature_id": random.randint(10000, 99999),
                    "rev": 1,
                    "signature": line_parts[6],
                    "category": "DNS Attack",
                    "severity": random.randint(1,2)
                },
                "payload_printable": f"Fake Payload: {line_parts[6]} from {line_parts[1]}",
                "stream": 0,
                "packet": line_parts[2],
                "packet_info": { "linktype": 1 }
        }

        try:

            response = requests.post(VECTOR_URL, json=event)
            if response.status_code == 200:
                print(f"[{time.strftime('%H:%M:%S')}] Sent: {template['signature']} from {template['country']} ({src})")
            else:
                print(f"Vector Rejected: {response.status_code} - {response.text}")
        
        except Exception as e:
            print(f"Error sending log: {e}")

        time.sleep(random.uniform(0.1, 1.0))

def generate_ip():

    return ".".join(str(random.randint(1, 254)) for _ in range(4))

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

def process_line(line):

    # Splits line into into 5 fields
    parts = line.strip().split()

    # If not split into fields return the line
    if len(parts) != 5:

        return line

    client_ip, query_type, domain, _, response_code = parts

    # If the domain from the line is in the ip map, replace the current ip with the one from the map
    if domain in domain_ip_map:

        resolved_ip = domain_ip_map[domain]

    # If the domain is not in the ip map, generate a new ip and add the domain into the ip map with the new ip
    else:

        resolved_ip = generate_ip()

        domain_ip_map[domain] = resolved_ip

    # Return the line with the new ip address
    return f"{client_ip} {query_type} {domain} {resolved_ip} {response_code}"

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

def DHCP_log(logtype):
    if logtype == 1:
        SIMULATION_MODE = "normal"
    elif logtype == 2:
        SIMULATION_MODE = "starvation"
    elif logtype == 3:
        SIMULATION_MODE = "spoofing"
    else:
        print("Not an option")
        return

    session_ip = generate_ip()

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

        prompt_extra = f"Provide exactly the IPs requested. Row 1: {session_ip}, Row 2: {generate_ip()}"

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

def DNS_log(attacktype):

    line_count = 0

    attack_line_position = []

    attack_lines = []

    max_line_count = 100

    DDOS_start = random.randint(0, max_line_count - 20)

    full_log = ""

    timestamp = "2025-10-01T12:00:00Z"

    def_prompt = "Forget all previous conversations. You are a DNS log generator. Generate exactly 1 line of a DNS log in the following format, and in this format only: <client_ip> <query_type> <domain> <resolved_ip> <response_code>. Do not include a timestamp. The line must be realistic, can include A or MX queries, and a variety of response codes (e.g., 200, 404, 502, 505). Important rules: Output only raw log lines, with no commentary, explanations, or headings. Do not wrap logs in code blocks. Only generate a single line."

    prompt = "No attack"

    web_list = ["google.com", "zoom.us", "teams.microsoft.com", "outlook.com", "gmail.com", "linkedin.com", "github.com", "stackoverflow.com", "youtube.com", "cnn.com", "nytimes.com", "bbc.com"]

    web_attack_prompt = "Only use domains from the following list: google.com, zoom.us, teams.microsoft.com, outlook.com, gmail.com, linkedin.com, github.com, stackoverflow.com, youtube.com, cnn.com, nytimes.com, bbc.com"

    web_def_prompt = "Use the following domain in the log line: "

    pattern = re.compile(

        r"(?:^)?"                                        # Optional newline or space

        r"\s+\d{1,3}(?:\.\d{1,3}){3}"                    # Client IPv4

        r"\s+(A|ANY|AAAA|CNAME|MX|NS|PTR|SOA|TXT)"       # Query type (flexible)

        r"\s+[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"               # Domain

        r"\s+(?:\d{1,3}(?:\.\d{1,3}){3}|[0-9a-fA-F:]+)"  # Resolved IP (IPv4 or IPv6)

        r"\s+\d+\b"                                      # Response code or port

    )

    if attacktype == 1:

        prompt = "Forget all previous conversations. You are a DNS log generator. Simulate DNS hijacking in exactly 20 DNS log lines using the following format: <client_ip> <query_type> <domain> <resolved_ip> <response_code>. The logs should show domain names resolving to suspicious or unexpected IPs, suggesting malicious redirection. Include only hijacked entries. Rules: Use the names of real websites in the log. Output only raw log lines, no commentary, headings, or code blocks. Do not output anything aside from the data in the log. Begin directly with the first log line. End after exactly 20 log lines."
        
        attack = "DNS_Hijacking"

    elif attacktype == 2:

        prompt = "Forget all previous conversations. You are a DNS log generator. Generate 20 raw DNS log lines that suggest DNS cache poisoning. Use the format: <client_ip> <query_type> <domain> <resolved_ip> <response_code>. The logs should include conflicting IPs for the same domain within a short time, unusually short TTL behavior (implied), or domains resolving to untrusted or unexpected IPs. Strict constraints: Use the names of real websites for realism. No explanation, no extra text. No code blocks. Only 20 properly formatted log lines. Do not label logs in any way."

        attack = "DNS_Cache_Poisoning"

    elif attacktype == 3:

        prompt = "Forget all previous conversations. You are a DNS log generator. Create 20 DNS log entries that show signs of a DNS amplification DDoS attack using the following format: <client_ip> <query_type> <domain> <resolved_ip> <response_code>. Simulate high-frequency queries from spoofed IPs, often using ANY or A record types to domains that would yield large responses. Use the names of real websites for realism. Format rules: No extra text or wrapping—just 20 raw logs in the exact structure shown. Begin with the first log line, stop after the 20th."

        attack = "DDDOS"

    elif attacktype == 4:

        prompt = "Forget all previous conversations. You are a DNS log generator. Generate 20 DNS log lines that reflect DNS tunneling activity using the format: <client_ip> <query_type> <domain> <resolved_ip> <response_code>. Include suspiciously long or encoded-looking subdomains, repetitive client queries, and suspicious target domains. Keep query types mostly as A. Use the names of real websites for realism and make the URLs look realistic. Strict rules: Output only the 20 raw lines. No explanations, formatting, or extra lines. Start immediately and stop at exactly 20."

        attack = "DNS_Tunneling"

    elif attacktype == 5:

        prompt = "Forget all previous conversations. You are a DNS log generator. Produce 20 DNS log entries showing signs of a fast flux network using the format: <client_ip> <query_type> <domain> <resolved_ip> <response_code>. Simulate the same domain resolving to many different IPs within short time intervals. Include multiple domains doing this, use response codes like 200 or 404, and use the names of real websites for realism. Output rules: Only raw DNS log lines in the exact format. No commentary or formatting. Limit output to exactly 20 lines. Do not use example.com, example.net, or any url like that."

        attack = "Fast_Flux"

    elif attacktype == 6:

        prompt = "No attack"

        attack = "No_Attack"

    else:

        print("That is not a valid input")

        return

    print("getting response from mistral")

    if attacktype == 3:

        # Different prompt for DDOS attack
        reply = chat_with_mistral(prompt + " " + web_def_prompt + web_list[random.randint(0,11)])

    else:

        reply = chat_with_mistral(prompt + " " + web_attack_prompt)

    # Filter the response through regex to make sure it has the correct formatting
    full_matches = [m.group(0) for m in pattern.finditer(reply)]

    # Put the lines into a list
    for log in full_matches:
        attack_lines.append(log)

    # Get random positions for attack lines
    attack_line_position = random.sample(range(max_line_count), len(attack_lines))
    
    # Runs until line_count equals max_line_count
    while line_count < max_line_count:

        # If an attack other than DDOS is selected
        if line_count in attack_line_position and attacktype != 3:

            # Remove newlines and spaces at the front a back of the response
            new_log = attack_lines[0].lstrip('\n')

            new_log = new_log.lstrip(' ')

            # Remove the added attack line
            attack_lines.pop(0)

            timestamp = datetime.utcnow().isoformat() + "Z"

            full_log = full_log + timestamp + " " + new_log + " " + attack + "\n"

            line_count = line_count + 1

        # If DDOS is selected
        elif attacktype == 3 and line_count == DDOS_start:
            
            for line in attack_lines:

                # Process the line
                new_line = line.lstrip('\n')

                new_line = new_line.lstrip(' ')

                new_line = process_line(new_line)

                timestamp = datetime.utcnow().isoformat() + "Z"

                full_log = full_log + timestamp + " " + new_line + " " +  attack + "\n"

                line_count = line_count + 1

        # If no attack is selected
        else:
            reply = chat_with_mistral(def_prompt + " " + web_def_prompt + web_list[random.randint(0,11)])

            # Filter responses through regex
            full_matches = [m.group(0) for m in pattern.finditer(reply)]

            try:
            
                # Take and process the first full match from the response
                log_str = full_matches[0].lstrip(' ')

                log_str = log_str.lstrip('\n')

                log_str = process_line(log_str)

                timestamp = datetime.utcnow().isoformat() + "Z"

                full_log = full_log + timestamp + " " + log_str + " " + "No_Attack" + "\n"
                
                line_count = line_count + 1

            except Exception as e:
                pass

    send_dns_traffic(full_log)

if __name__ == "__main__":
    loops = 4

    while 1 == 1:
        # Gets log type
        logtype = random.randint(1,2)

        if logtype == 1:
            attacktype = random.randint(1,6)
            DNS_log(attacktype)
        elif logtype == 2:
            attacktype = random.randint(1,3)
            DHCP_log(attacktype)
        else:
            print("That is not a valid input")
            exit()
