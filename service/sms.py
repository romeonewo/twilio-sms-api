# sms.py
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

INFOBIP_BASE_URL = os.getenv("INFOBIP_BASE_URL")
INFOBIP_API_KEY = os.getenv("INFOBIP_API_KEY")
INFOBIP_FROM = os.getenv("INFOBIP_FROM")


def send_sms(to: str, text: str) -> dict:
    url = f"https://{INFOBIP_BASE_URL}/sms/2/text/advanced"
    headers = {
        "Authorization": f"App {INFOBIP_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {
        "messages": [
            {
                "from": INFOBIP_FROM,
                "destinations": [{"to": to}],
                "text": text
            }
        ]
    }

    response = httpx.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Infobip Error: {response.status_code} - {response.text}")

    return response.json()
