import http.client
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE = os.getenv("INFOBIP_API_BASE")
API_KEY = os.getenv("INFOBIP_API_KEY")
SENDER = os.getenv("INFOBIP_SENDER_NUMBER")

def send_sms(to: str, message: str) -> dict:
    conn = http.client.HTTPSConnection(API_BASE)

    payload = json.dumps({
        "messages": [
            {
                "destinations": [{"to": to}],
                "from": SENDER,
                "text": message
            }
        ]
    })

    headers = {
        'Authorization': f'App {API_KEY}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    conn.request("POST", "/sms/2/text/advanced", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))
