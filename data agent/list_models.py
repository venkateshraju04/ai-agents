import os
from dotenv import load_dotenv
import requests

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

headers = {
    "Authorization": f"Bearer {api_key}",
}

response = requests.get("https://api.groq.com/openai/v1/models", headers=headers)
if response.status_code == 200:
    models = response.json().get("data", [])
    for model in models:
        print(model["id"])
else:
    print(f"Error: {response.status_code}")
    print(response.text)
