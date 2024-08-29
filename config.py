from dotenv import load_dotenv
import os
import asyncio

# ---------------------------------------------------------------------
# Load environment variables from .env file
# ---------------------------------------------------------------------


load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
RECIPIENT_WA_ID = os.getenv("RECIPIENT_WA_ID")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERSION = os.getenv("VERSION")

APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")
# Configuration variable, replace with your actual verify token
CONFIG_VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")