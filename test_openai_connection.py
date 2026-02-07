import os
import httpx
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY").strip()

print(f"API Key prefix: {api_key[:8]}..." if api_key else "No API Key")

# Custom HTTP client to debug
http_client = httpx.Client(verify=True) # Explicitly set verify

try:
    client = OpenAI(api_key=api_key, http_client=http_client)
    print("Attempting to connect to OpenAI via Client...")
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hi"}],
        max_tokens=5
    )
    print("SUCCESS")
    print(response.choices[0].message.content)
except Exception as e:
    print("\nFAILED")
    print(f"Error: {e}")
    if hasattr(e, '__cause__'):
        print(f"Cause: {e.__cause__}")
