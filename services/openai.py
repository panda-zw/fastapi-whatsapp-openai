import asyncio
import time

from openai import OpenAI, APIConnectionError
import shelve
from dotenv import load_dotenv
import os
import logging

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID")
client = OpenAI(api_key=OPENAI_API_KEY)

async def upload_file(path):
    file = client.files.create(
        file=open(path, "rb"), purpose="assistants"
    )
    return file

async def create_assistant(file):
    assistant = client.beta.assistants.create(
        name="WhatsApp AirBnb Assistant",
        instructions="You're a helpful WhatsApp assistant that can assist guests that are staying in our Paris AirBnb. Use your knowledge base to best respond to customer queries. If you don't know the answer, say simply that you cannot help with question and advice to contact the host directly. Be friendly and funny.",
        tools=[{"type": "retrieval"}],
        model="gpt-4-1106-preview",
        file_ids=[file.id],
    )
    return assistant

async def check_if_thread_exists(wa_id):
    with shelve.open("threads_db") as threads_shelf:
        return threads_shelf.get(wa_id, None)

async def store_thread(wa_id, thread_id):
    with shelve.open("threads_db", writeback=True) as threads_shelf:
        threads_shelf[wa_id] = thread_id

async def wait_for_run_completion(thread):
    """
    Wait for any active run associated with the thread to complete.
    """
    timeout = 60  # seconds
    start_time = time.time()

    while True:
        run_list = client.beta.threads.runs.list(thread_id=thread.id)
        active_runs = [run for run in run_list.data if run.status in ["queued", "in_progress"]]

        if not active_runs:
            break

        if time.time() - start_time > timeout:
            raise TimeoutError("Waiting for run to complete timed out")

        await asyncio.sleep(1)  # Wait a bit before checking again

async def run_assistant(thread, name):
    try:
        print("Running assistant")
        assistant = client.beta.assistants.retrieve(OPENAI_ASSISTANT_ID)
        print("Assistant retrieved")

        # Wait for any active run to complete
        await wait_for_run_completion(thread)

        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )

        print(f"Initial run status: {run.status}")

        timeout = 60  # seconds
        start_time = time.time()

        while run.status != "completed":
            if time.time() - start_time > timeout:
                raise TimeoutError("Assistant run timed out")

            await asyncio.sleep(0.5)
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            print(f"Run status: {run.status}")

        if run.status == "failed":
            raise RuntimeError("Assistant run failed")

        messages = client.beta.threads.messages.list(thread_id=thread.id)
        new_message = messages.data[0].content[0].text.value
        logging.info(f"Generated message: {new_message}")
        return new_message

    except APIConnectionError as e:
        logging.error(f"API Connection Error: {e}")
        raise e
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise e

async def generate_response(message_body, wa_id, name):
    print("Generating response")
    thread_id = await check_if_thread_exists(wa_id)

    if thread_id is None:
        logging.info(f"Creating new thread for {name} with wa_id {wa_id}")
        thread = client.beta.threads.create()
        await store_thread(wa_id, thread.id)
        thread_id = thread.id
    else:
        logging.info(f"Retrieving existing thread for {name} with wa_id {wa_id}")
        thread = client.beta.threads.retrieve(thread_id)

    # Ensure no active runs before adding a new message
    await wait_for_run_completion(thread)

    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message_body,
    )

    new_message = await run_assistant(thread, name)
    return new_message
