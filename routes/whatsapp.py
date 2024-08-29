from fastapi import APIRouter, HTTPException, Body, Request, Query
import json
import requests

from config import VERSION, PHONE_NUMBER_ID, ACCESS_TOKEN, RECIPIENT_WA_ID, CONFIG_VERIFY_TOKEN
from controllers.whatsapp import handle_message

router = APIRouter()


@router.post("/send_test_message")
async def send_whatsapp_message():
    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": "Bearer " + ACCESS_TOKEN,
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": RECIPIENT_WA_ID,
        "type": "template",
        "template": {"name": "hello_world", "language": {"code": "en_US"}}
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()


@router.get("/webhooks")
async def messaging_webhook(
    mode: str = Query(None, alias="hub.mode"),
    token: str = Query(None, alias="hub.verify_token"),
    challenge: str = Query(None, alias="hub.challenge")
):
    # Check if mode and token are present in the query string
    if mode and token:
        # Check if the mode is 'subscribe' and the token matches the config token
        if mode == "subscribe" and token == CONFIG_VERIFY_TOKEN:
            # Log the verification and respond with the challenge
            print("WEBHOOK_VERIFIED")
            # Challenge must be returned as an int
            return int(challenge)
        else:
            # Respond with '403 Forbidden' if the token does not match
            raise HTTPException(status_code=403)
    # If mode or token are missing, return '400 Bad Request'
    raise HTTPException(status_code=400)


@router.post("/webhooks")
async def webhook_post(request: Request):
    return await handle_message(request)

