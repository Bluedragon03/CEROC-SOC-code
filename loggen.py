import requests
import re
import random
from datetime import datetime, timedelta

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

def generate_ip():

    return ".".join(str(random.randint(1, 254)) for _ in range(4))

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

def DNS_log():

    line_count = 0

    attack_start = 0

    max_line_count = 100

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

    # Get the attack that appears in the log and set the prompt
    attacktype = int(input("Please select an attack:\n1. DNS Hijacking\n2. DNS Cache Poisoning\n3. DDoS\n4. DNS Tunneling\n5. Fast Flux Attack\n6. No Attack\n"))

    if attacktype == 1:

        prompt = "Forget all previous conversations. You are a DNS log generator. Simulate DNS hijacking in exactly 20 DNS log lines using the following format: <client_ip> <query_type> <domain> <resolved_ip> <response_code>. The logs should show domain names resolving to suspicious or unexpected IPs, suggesting malicious redirection. Include only hijacked entries. Rules: Use the names of real websites in the log. Output only raw log lines, no commentary, headings, or code blocks. Do not output anything aside from the data in the log. Begin directly with the first log line. End after exactly 20 log lines."

    elif attacktype == 2:

        prompt = "Forget all previous conversations. You are a DNS log generator. Generate 20 raw DNS log lines that suggest DNS cache poisoning. Use the format: <client_ip> <query_type> <domain> <resolved_ip> <response_code>. The logs should include conflicting IPs for the same domain within a short time, unusually short TTL behavior (implied), or domains resolving to untrusted or unexpected IPs. Strict constraints: Use the names of real websites for realism. No explanation, no extra text. No code blocks. Only 20 properly formatted log lines. Do not label logs in any way."

    elif attacktype == 3:

        prompt = "Forget all previous conversations. You are a DNS log generator. Create 20 DNS log entries that show signs of a DNS amplification DDoS attack using the following format: <client_ip> <query_type> <domain> <resolved_ip> <response_code>. Simulate high-frequency queries from spoofed IPs, often using ANY or A record types to domains that would yield large responses. Use the names of real websites for realism. Format rules: No extra text or wrapping—just 20 raw logs in the exact structure shown. Begin with the first log line, stop after the 20th."

    elif attacktype == 4:

        prompt = "Forget all previous conversations. You are a DNS log generator. Generate 20 DNS log lines that reflect DNS tunneling activity using the format: <client_ip> <query_type> <domain> <resolved_ip> <response_code>. Include suspiciously long or encoded-looking subdomains, repetitive client queries, and suspicious target domains. Keep query types mostly as A. Use the names of real websites for realism and make the URLs look realistic. Strict rules: Output only the 20 raw lines. No explanations, formatting, or extra lines. Start immediately and stop at exactly 20."

    elif attacktype == 5:

        prompt = "Forget all previous conversations. You are a DNS log generator. Produce 20 DNS log entries showing signs of a fast flux network using the format: <client_ip> <query_type> <domain> <resolved_ip> <response_code>. Simulate the same domain resolving to many different IPs within short time intervals. Include multiple domains doing this, use response codes like 200 or 404, and use the names of real websites for realism. Output rules: Only raw DNS log lines in the exact format. No commentary or formatting. Limit output to exactly 20 lines. Do not use example.com, example.net, or any url like that."

    elif attacktype == 6:

        prompt = "No attack"

    else:

        print("That is not a valid input")

        return

    print("getting response from mistral")

    # Get the line the attack starts on
    attack_start = random.randint(1, max_line_count - 25)
    
    # Runs until line_count equals max_line_count
    while line_count < max_line_count:

        # If an attack is selected
        if line_count == attack_start and prompt != "No attack":

            if attacktype == 3:

                # Different prompt for DDOS attack
                reply = chat_with_mistral(prompt + " " + web_def_prompt + web_list[random.randint(0,11)])
            
            else:
                
                reply = chat_with_mistral(prompt + " " + web_attack_prompt)

            # Filter the response through regex to make sure it has the correct formatting
            full_matches = [m.group(0) for m in pattern.finditer(reply)]

            for log in full_matches:

                # Increment the timestamp by 1 second
                dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")

                dt += timedelta(seconds=1)

                timestamp_str = dt.strftime("%Y-%m-%dT%H:%M:%SZ")

                # Remove newlines and spaces at the front a back of the response
                new_log = log.lstrip('\n')

                new_log = new_log.lstrip(' ')

                if attacktype == 3:

                    # Adjust ip addresses if attack is DDOS
                    new_log = process_line(new_log)

                # Print output to outputlog.txt for practice use
                with open('outputlog.txt', 'a') as file:
                    file.write(timestamp)
                    file.write(" ")
                    file.write(new_log)
                    file.write("\n")
                
                # Print output to answeroutputlog.txt for the purpose of checking if the user found the correct attack lines
                with open('answeroutputlog.txt', 'a') as file:
                    file.write(timestamp)
                    file.write(" ")
                    file.write(new_log)
                    file.write(" ")
                    file.write("suspicious")
                    file.write("\n")

                line_count = line_count + 1

        # If no attack is selected
        else:
            reply = chat_with_mistral(def_prompt + " " + web_def_prompt + web_list[random.randint(0,11)])

            # Filter responses through regex
            full_matches = [m.group(0) for m in pattern.finditer(reply)]

            try:

                # Increment timestamp by 1 second
                dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")

                dt += timedelta(seconds=1)

                timestamp = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
            
                # Take and process the first full match from the response
                log_str = full_matches[0].lstrip(' ')

                log_str = log_str.lstrip('\n')

                log_str = process_line(log_str)

                # Print output to practice log and answer key log
                with open('outputlog.txt', 'a') as file:
                    file.write(timestamp)
                    file.write(" ")
                    file.write(log_str)
                    file.write("\n")

                with open('answeroutputlog.txt', 'a') as file:
                    file.write(timestamp)
                    file.write(" ")
                    file.write(log_str)
                    file.write("\n")
                
                line_count = line_count + 1

            except:
                # Decrement timestamp by 1 second if no valid log line is generated
                dt -= timedelta(seconds=1)

    print("printing reply to outputlog.txt and an answer key has been printed to answeroutputlog.txt")

if __name__ == "__main__":

    # Clear the contents of outputlog.txt and answeroutputlog.txt
    with open('outputlog.txt', 'w'):
        
        pass
    
    with open('answeroutputlog.txt', 'w'):

        pass
    
    # Gets log type
    logtype = int(input("Please select a type of log:\n1. DNS\n"))

    if logtype == 1:

        DNS_log()

    else:

        print("That is not a valid input")
        
        exit()
