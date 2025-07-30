import requests
import re
from datetime import datetime, timedelta


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

    pattern = re.compile(

        r"\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z"        # Timestamp

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

        prompt = "Forget all previous conversations. You are a DNS log generator. Generate exactly 50 lines of DNS log entries in the following format, and in this format only: YYYY-MM-DDTHH:MM:SSZ <client_ip> <query_type> <domain> <resolved_ip> <response_code>. Each line must be realistic, use RFC3339 timestamps, and include a mix of A and MX queries, subdomains, and a variety of IPs and response codes (e.g., 200, 404, 502, 505). Use the names of real websites for realism. Even for MX queries, the <resolved_ip> field must be an IPv4 address, not a domain name. Assume the MX hostname has already been resolved. Important rules: Output only raw log lines, with no commentary, explanations, or headings. Do not wrap logs in code blocks. Start immediately with the first log line. Stop after exactly 50 log lines. Do not use example.com, example.net or other similar urls."

    else:

        print("That is not a valid input")

        return

    print("getting response from mistral")

    reply = chat_with_mistral(prompt)

    print("printing reply to outputlog.txt")

    full_matches = [m.group(0) for m in pattern.finditer(reply)]

    with open('outputlog.txt', 'w') as file:

        for log in full_matches:
            file.write(log)
            file.write("\n")

if __name__ == "__main__":

    with open('outputlog.txt', 'w'):
        
        pass
    
    logtype = int(input("Please select a type of log:\n1. DNS\n"))

    if logtype == 1:

        DNS_log()

    else:

        print("That is not a valid input")
        
        exit()
