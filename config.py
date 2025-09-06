import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "lm-studio")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "http://localhost:1234/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "google/gemma-3-1b")

# Enable/disable streaming responses
STREAM_MODE = os.getenv("STREAM_MODE", "false").lower() == "true"
