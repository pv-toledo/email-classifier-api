import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("Chave da API do Google não encontrada. Verifique o .env")

ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
