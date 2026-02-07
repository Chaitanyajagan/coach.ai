import httpx
import time

def check(url):
    print(f"Checking {url}...")
    try:
        response = httpx.get(url, timeout=5.0)
        print(f"SUCCESS: {url} returned {response.status_code}")
    except Exception as e:
        print(f"FAILED: {url} - {str(e)}")

print("--- Network Connectivity Check ---")
check("https://www.google.com")
check("https://api.openai.com")
