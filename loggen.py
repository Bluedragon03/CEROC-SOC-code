import requests
import re
import random
from datetime import datetime, timedelta

domain_ip_map = {}

def generate_ip():

    return ".".join(str(random.randint(1, 254)) for _ in range(4))

def process_line(line):

    parts = line.strip().split()

    if len(parts) != 5:

        return line

    client_ip, query_type, domain, _, response_code = parts

    if domain in domain_ip_map:

        resolved_ip = domain_ip_map[domain]

    else:

        resolved_ip = generate_ip()

        domain_ip_map[domain] = resolved_ip

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

    timestamp = "2025-10-01T12:00:01Z"

    def_prompt = "Forget all previous conversations. You are a DNS log generator. Generate exactly 1 line of a DNS log in the following format, and in this format only: <client_ip> <query_type> <domain> <resolved_ip> <response_code>. Do not include a timestamp. The line must be realistic, use the name of a real website, and can include A or MX queries, and a variety of IPs and response codes (e.g., 200, 404, 502, 505). Important rules: Output only raw log lines, with no commentary, explanations, or headings. Do not wrap logs in code blocks. Only generate a single line. Do not use any example domains (domains that include the word 'example' in any way). Do not use search engines, like google or yahoo, as domains."

    prompt = "No attack"

    pattern = re.compile(

        r"(?:^)?"

        r"\s+\d{1,3}(?:\.\d{1,3}){3}"                    # Client IPv4

        r"\s+(A|ANY|AAAA|CNAME|MX|NS|PTR|SOA|TXT)"       # Query type (flexible)

        r"\s+[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"               # Domain

        r"\s+(?:\d{1,3}(?:\.\d{1,3}){3}|[0-9a-fA-F:]+)"  # Resolved IP (IPv4 or IPv6)

        r"\s+\d+\b"                                      # Response code or port

    )

    attacktype = int(input("Please select an attack:\n1. DNS Hijacking\n2. DNS Cache Poisoning\n3. DDoS\n4. DNS Tunneling\n5. Fast Flux Attack\n6. No Attack\n"))

    if attacktype == 1:

        prompt = "Forget all previous conversations. You are a DNS log generator. Simulate DNS hijacking in exactly 50 DNS log lines using the following format: YYYY-MM-DDTHH:MM:SSZ <client_ip> <query_type> <domain> <resolved_ip> <response_code>. The logs should show domain names resolving to suspicious or unexpected IPs, suggesting malicious redirection. Include a mix of normal and hijacked entries for realism. Rules: Use the names of real websites in the log. Output only raw log lines, no commentary, headings, or code blocks. Do not output anything aside from the data in the log. Begin directly with the first log line. End after exactly 50 log lines."

    elif attacktype == 2:

        prompt = "Forget all previous conversations. You are a DNS log generator. Generate 50 raw DNS log lines that suggest DNS cache poisoning. Use the format: YYYY-MM-DDTHH:MM:SSZ <client_ip> <query_type> <domain> <resolved_ip> <response_code>. The logs should include conflicting IPs for the same domain within a short time, unusually short TTL behavior (implied), or domains resolving to untrusted or unexpected IPs. Strict constraints: Use the names of real websites for realism. No explanation, no extra text. No code blocks. Only 50 properly formatted log lines. Do not label logs in any way."

    elif attacktype == 3:

        prompt = "Forget all previous conversations. You are a DNS log generator. Create 50 DNS log entries that show signs of a DNS amplification DDoS attack using the following format: YYYY-MM-DDTHH:MM:SSZ <client_ip> <query_type> <domain> <resolved_ip> <response_code>. Simulate high-frequency queries from spoofed IPs, often using ANY or A record types to domains that would yield large responses. Use the names of real websites for realism. Format rules: No extra text or wrapping—just 50 raw logs in the exact structure shown. Begin with the first log line, stop after the 50th."

    elif attacktype == 4:

        prompt = "Forget all previous conversations. You are a DNS log generator. Generate 50 DNS log lines that reflect DNS tunneling activity using the format: YYYY-MM-DDTHH:MM:SSZ <client_ip> <query_type> <domain> <resolved_ip> <response_code>. Include suspiciously long or encoded-looking subdomains, repetitive client queries, and suspicious target domains. Keep query types mostly as A. Use the names of real websites for realism and make the URLs look realistic. Strict rules: Output only the 50 raw lines. No explanations, formatting, or extra lines. Start immediately and stop at exactly 50."

    elif attacktype == 5:

        prompt = "Forget all previous conversations. You are a DNS log generator. Produce 50 DNS log entries showing signs of a fast flux network using the format: YYYY-MM-DDTHH:MM:SSZ <client_ip> <query_type> <domain> <resolved_ip> <response_code>. Simulate the same domain resolving to many different IPs within short time intervals. Include multiple domains doing this, use response codes like 200 or 404, and use the names of real websites for realism. Output rules: Only raw DNS log lines in the exact format. No commentary or formatting. Limit output to exactly 50 lines. Do not use example.com, example.net, or any url like that."

    elif attacktype == 6:

        prompt = "No attack"

    else:

        print("That is not a valid input")

        return

    print("getting response from mistral")

    attack_start = random.randint(1, max_line_count - 25)
    
    while line_count < max_line_count:

        if line_count == attack_start and prompt != "No attack":

            reply = chat_with_mistral(prompt)

            full_matches = [m.group(0) for m in pattern.finditer(reply)]

            for log in full_matches:

                dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")

                dt += timedelta(seconds=1)

                timestamp_str = dt.strftime("%Y-%m-%dT%H:%M:%SZ")

                new_log = log.lstrip('\n')

                new_log = new_log.lstrip(' ')

                with open('outputlog.txt', 'a') as file:
                    file.write(timestamp)
                    file.write(" ")
                    file.write(new_log)
                    file.write("\n")

                line_count = line_count + 1

        else:
            reply = chat_with_mistral(def_prompt)

            full_matches = [m.group(0) for m in pattern.finditer(reply)]

            dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")

            dt += timedelta(seconds=1)

            timestamp = dt.strftime("%Y-%m-%dT%H:%M:%SZ")

            log_str = full_matches[0].lstrip(' ')

            log_str = log_str.lstrip('\n')

            log_str = process_line(log_str)

            with open('outputlog.txt', 'a') as file:
                file.write(timestamp)
                file.write(" ")
                file.write(log_str)
                file.write("\n")

            line_count = line_count + 1

    print("printing reply to outputlog.txt")

if __name__ == "__main__":

    with open('outputlog.txt', 'w'):
        
        pass
    
    logtype = int(input("Please select a type of log:\n1. DNS\n"))

    if logtype == 1:

        DNS_log()

    else:

        print("That is not a valid input")
        
        exit()
