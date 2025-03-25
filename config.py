import os
from dotenv import load_dotenv

load_dotenv()  # Load .env variables if present

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
