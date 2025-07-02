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


if __name__ == "__main__":
    
    logtype = int(input("Please select a type of log:\n1. DNS\n"))

    if logtype == 1:

        attacktype = int(input("Please select an attack:\n1. DNS Hijacking\n2. DNS Cache Poisoning\n3. DDoS\n4. DNS Tunneling\n5. Fast Flux Attack\n6. No Attack\n"))
        
        if attacktype == 1:
        
            prompt = "Generate exactly 50 lines of realistic DNS log entries showing signs of DNS hijacking. Include unusual or suspicious redirections where domain names resolve to unexpected or malicious IP addresses. Each log line should include a timestamp, client IP, query type, domain name, resolved IP, and response code. Output only the raw log lines—no explanation or extra text."
        
        elif attacktype == 2:
        
            prompt = "Generate exactly 50 lines of DNS server log data that indicate DNS cache poisoning attempts. Include conflicting responses for the same domain, unusually short TTLs, or spoofed responses from non-authoritative servers. Each log line must include a timestamp, client IP, query type, domain name, and the (potentially malicious) resolved IP. Do not include any headers or extra explanation—only raw log lines."
        
        elif attacktype == 3:
        
            prompt = "Generate exactly 50 lines of DNS log data showing signs of a DNS amplification DDoS attack. Include a high volume of similar queries from spoofed IP addresses, often with large query responses (e.g., ANY requests). Each log line should include a timestamp, client IP, query type, domain, and response size. Return only raw log entries with no additional explanation. Do not include any explanation, headers, or comments—only the 50 lines of raw log data."
        
        elif attacktype == 4:
        
            prompt = "Generate exactly 50 lines of DNS log entries that suggest DNS tunneling activity. Use long, encoded subdomain names, repetitive queries to specific domains, and unusual query patterns. Each log line should contain a timestamp, client IP, query type, domain name, and response code. Return only raw logs—no summaries or added text."
        
        elif attacktype == 5:
        
            prompt = "Generate exactly 50 lines of DNS log entries showing evidence of a fast flux network. The same domain name should resolve to many different IP addresses in rapid succession, often with low TTLs. Include timestamps, client IPs, domain names, resolved IPs, and TTLs. Output only raw log lines—no explanation or formatting beyond the logs."
        
        elif attacktype == 6:
        
            prompt = "Generate exactly 50 lines of realistic DNS log entries. Each line should resemble output from a DNS server log, including a timestamp, client IP address, query type, domain name, and response code. Do not include any explanation, headers, or comments—only the 50 lines of raw log data."
        
        else:
        
            print("That is not a valid input")
            
            exit()
    
    else:
       
        print("That is not a valid input")
        
        exit()

    print("getting response from mistral")
    
    reply = chat_with_mistral(prompt)

    print("printing reply to outputlog.txt")

    with open('outputlog.txt', 'w') as file:

        file.write(reply)

        file.write("\n")
