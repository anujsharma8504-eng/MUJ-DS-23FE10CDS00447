import os
import time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

key = os.getenv("GEMINI_API_KEY")
print(f"[1] Key loaded: {key[:10]}...")

client = OpenAI(
    api_key=key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Try these models in order until one works
MODELS = [
    "gemini-3.8-flash",
    "gemini-2.5-flash",
    "gemini-2.0-flash",
]

response = None
for model in MODELS:
    try:
        print(f"[2] Trying model: {model} ...")
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Reply with exactly: Hello, Gemini is working!"},
            ],
            temperature=0,
        )
        print(f"[3] ✅ Success with model: {model}")
        break
    except Exception as e:
        print(f"[!] Failed with {model}: {type(e).__name__}")
        # If it's a 503 (busy), wait and retry once
        if "503" in str(e):
            print("    Server busy, waiting 5 seconds...")
            time.sleep(5)
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": "Reply with exactly: Hello, Gemini is working!"},
                    ],
                    temperature=0,
                )
                print(f"[3] ✅ Success on retry with: {model}")
                break
            except Exception as e2:
                print(f"[!] Retry failed: {type(e2).__name__}")

if response:
    print("[4] Content:", response.choices[0].message.content)
else:
    print("[X] All models failed. Try again in a minute.")