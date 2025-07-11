import requests
import re


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


if __name__ == "__main__":

    pattern = re.compile(

    r"\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z"      # Timestamp

    r"\s+\d{1,3}(?:\.\d{1,3}){3}"                  # Client IP

    r"\s+[A-Z]+"                                   # Query type (A, AAAA, MX, etc.)

    r"\s+[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"             # Domain

    r"\s+\d{1,3}(?:\.\d{1,3}){3}"                  # Resolved IP

    r"\s+\d{3}\b"                                  # Response code (e.g., 404, 200)

    )
    
    logtype = int(input("Please select a type of log:\n1. DNS\n"))

    if logtype == 1:

        attacktype = int(input("Please select an attack:\n1. DNS Hijacking\n2. DNS Cache Poisoning\n3. DDoS\n4. DNS Tunneling\n5. Fast Flux Attack\n6. No Attack\n"))
        
        if attacktype == 1:
        
            prompt = "Forget all previous conversations. You are a DNS log generator. Simulate DNS hijacking in exactly 50 DNS log lines using the following format: YYYY-MM-DDTHH:MM:SSZ <client_ip> <query_type> <domain> <resolved_ip> <response_code>. The logs should show domain names resolving to suspicious or unexpected IPs, suggesting malicious redirection. Include a mix of normal and hijacked entries for realism. Rules: Use the names of real websites in the log. Output only raw log lines, no commentary, headings, or code blocks. Do not output anything aside from the data in the log. Begin directly with the first log line. End after exactly 50 log lines."
        
        elif attacktype == 2:
        
            prompt = "Forget all previous conversations. You are a DNS log generator. Generate 50 raw DNS log lines that suggest DNS cache poisoning. Use the format: YYYY-MM-DDTHH:MM:SSZ <client_ip> <query_type> <domain> <resolved_ip> <response_code>. The logs should include conflicting IPs for the same domain within a short time, unusually short TTL behavior (implied), or domains resolving to untrusted or unexpected IPs. Strict constraints: Use the names of real websites for realism. No explanation, no extra text. No code blocks. Only 50 properly formatted log lines. Do not label logs in any way."
        
        elif attacktype == 3:
        
            prompt = "Forget all previous conversations. You are a DNS log generator. Create 50 DNS log entries that show signs of a DNS amplification DDoS attack using the following format: YYYY-MM-DDTHH:MM:SSZ <client_ip> <query_type> <domain> <resolved_ip> <response_code>. Simulate high-frequency queries from spoofed IPs, often using ANY or A record types to domains that would yield large responses. Include a mix of normal and suspicious entriesfor realism. Rules: Use the names of real websites in the log. Output only raw log lines, no commentary, headings, or code blocks. Do not output anything aside from the data in the log. Begin directly with the first log line. End after exactly 50 log lines."
        
        elif attacktype == 4:
        
            prompt = "Forget all previous conversations. You are a DNS log generator. Generate 50 DNS log lines that reflect DNS tunneling activity using the format: YYYY-MM-DDTHH:MM:SSZ <client_ip> <query_type> <domain> <resolved_ip> <response_code>. Include suspiciously long or encoded-looking subdomains, repetitive client queries, and suspicious target domains. Keep query types mostly as A. Include a mix of normal and suspicious entriesfor realism. Rules: Use the names of real websites in the log. Output only raw log lines, no commentary, headings, or code blocks. Do not output anything aside from the data in the log. Begin directly with the first log line. End after exactly 50 log lines."
        
        elif attacktype == 5:
        
            prompt = "You are a DNS log generator. Produce 50 DNS log entries showing signs of a fast flux network using the format: YYYY-MM-DDTHH:MM:SSZ <client_ip> <query_type> <domain> <resolved_ip> <response_code>. Simulate the same domain resolving to many different IPs within short time intervals. Include multiple domains doing this, and use response codes like 200 or 404. Include a mix of normal and suspicious entriesfor realism. Rules: Use the names of real websites in the log. Output only raw log lines, no commentary, headings, or code blocks. Do not output anything aside from the data in the log. Begin directly with the first log line. End after exactly 50 log lines."
        
        elif attacktype == 6:
        
            prompt = "You are a DNS log generator. Generate exactly 50 lines of DNS log entries in the following format, and in this format only: YYYY-MM-DDTHH:MM:SSZ <client_ip> <query_type> <domain> <resolved_ip> <response_code>. Each line must be realistic, use RFC3339 timestamps, and include a mix of A and MX queries, subdomains, and a variety of IPs and response codes (e.g., 200, 404, 502, 505). Rules: Use the names of real websites in the log. Output only raw log lines, no commentary, headings, or code blocks. Do not output anything aside from the data in the log. Begin directly with the first log line. End after exactly 50 log lines."
        
        else:
        
            print("That is not a valid input")
            
            exit()
    
    else:
       
        print("That is not a valid input")
        
        exit()

    print("getting response from mistral")
    
    reply = chat_with_mistral(prompt)

    print("printing reply to outputlog.txt")

    valid_logs = pattern.findall(reply)

    print(reply)

    with open('outputlog.txt', 'w') as file:

        for log in valid_logs:
            file.write(log)
            file.write("\n")
