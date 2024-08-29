import json
import re

from fastapi import HTTPException
from starlette.responses import JSONResponse

from config import RECIPIENT_WA_ID, VERSION, PHONE_NUMBER_ID, ACCESS_TOKEN
import requests

from services.openai import generate_response


async def process_text_for_whatsapp(text):
    # Remove brackets
    pattern = r"\【.*?\】"
    # Substitute the pattern with an empty string
    text = re.sub(pattern, "", text).strip()

    # Pattern to find double asterisks including the word(s) in between
    pattern = r"\*\*(.*?)\*\*"

    # Replacement pattern with single asterisks
    replacement = r"*\1*"

    # Substitute occurrences of the pattern with the replacement
    whatsapp_style_text = re.sub(pattern, replacement, text)

    return whatsapp_style_text


async def process_whatsapp_message(body):
    wa_id = body["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
    name = body["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]

    message = body["entry"][0]["changes"][0]["value"]["messages"][0]
    message_body = message["text"]["body"]

    # TODO: implement custom function here
    # response = await generate_response(message_body)
    print("process_whatsapp_message")
    # OpenAI Integration
    response = await generate_response(message_body, wa_id, name)
    response = await process_text_for_whatsapp(response)

    data = await get_text_message_input(RECIPIENT_WA_ID, response)
    await send_message(data)


async def is_valid_whatsapp_message(body):
    """
    Check if the incoming webhook event has a valid WhatsApp message structure.
    """
    return (
        body.get("object")
        and body.get("entry")
        and body["entry"][0].get("changes")
        and body["entry"][0]["changes"][0].get("value")
        and body["entry"][0]["changes"][0]["value"].get("messages")
        and body["entry"][0]["changes"][0]["value"]["messages"][0]
    )


async def send_message(data):
    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": "Bearer " + ACCESS_TOKEN,
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.json())


async def handle_message(request):
    """
    Handle incoming webhook events from the WhatsApp API.

    This function processes incoming WhatsApp messages and other events,
    such as delivery statuses. If the event is a valid message, it gets
    processed. If the incoming payload is not a recognized WhatsApp event,
    an error is returned.

    Every message sent will trigger 4 HTTP requests to your webhook: message, sent, delivered, read.

    Returns:
        response: A JSON response.
    """
    try:
        body = await request.json()

        # Check if it's a WhatsApp status update
        if (
            body.get("entry", [{}])[0]
            .get("changes", [{}])[0]
            .get("value", {})
            .get("statuses")
        ):
            return JSONResponse(content={"status": "ok"}, status_code=200)

        # Process the message if it's a valid WhatsApp message
        if await is_valid_whatsapp_message(body):
            await process_whatsapp_message(body)
            return JSONResponse(content={"status": "ok"}, status_code=200)
        else:
            # If the request is not a WhatsApp API event, return an error
            return JSONResponse(
                content={"status": "error", "message": "Not a WhatsApp API event"},
                status_code=404
            )
    except ValueError:
        return JSONResponse(
            content={"status": "error", "message": "Invalid JSON provided"},
            status_code=400
        )


async def get_text_message_input(recipient, message):
    return {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": message
        }
    }
