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



# Example usage

if __name__ == "__main__":

    line = 0
    
    pattern = re.compile(

    #r"\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z"        # Timestamp

    r"\s+\d{1,3}(?:\.\d{1,3}){3}"                    # Client IPv4

    r"\s+(A|ANY|AAAA|CNAME|MX|NS|PTR|SOA|TXT)"       # Query type (flexible)

    r"\s+[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"               # Domain

    r"\s+(?:\d{1,3}(?:\.\d{1,3}){3}|[0-9a-fA-F:]+)"  # Resolved IP (IPv4 or IPv6)

    r"\s+\d+\b"                                      # Response code or port

    )

    timestamp_str = "2025-10-01T12:00:01Z"
    
    prompt = "Forget all previous conversations. You are a DNS log generator. Generate exactly 1 line of a DNS log in the following format, and in this format only: <client_ip> <query_type> <domain> <resolved_ip> <response_code>. Do not include a timestamp. The line must be realistic, and can include a mix of A and MX queries, subdomains, and a variety of IPs and response codes (e.g., 200, 404, 502, 505). Important rules: Output only raw log lines, with no commentary, explanations, or headings. Do not wrap logs in code blocks. Only generate a single line."

    while line != 61:
    
        reply = chat_with_mistral(prompt)

        full_matches = [m.group(0) for m in pattern.finditer(reply)]

        dt = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ")

        dt += timedelta(seconds=1)

        timestamp_str = dt.strftime("%Y-%m-%dT%H:%M:%SZ")

        print(timestamp_str, full_matches[0])

        line = line + 1
