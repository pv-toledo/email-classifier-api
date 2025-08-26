import os
import logging
import json
import google.generativeai as genai
from dotenv import load_dotenv
from cleantext import clean

from .prompt_templates import EMAIL_RESPONSE_PROMPT_TEMPLATE

load_dotenv()
logger = logging.getLogger(__name__)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Chave da API do Google não encontrada.")

genai.configure(api_key=GOOGLE_API_KEY)

def get_email_classification(email_text: str) -> dict:
 
    cleaned_text = clean(
        email_text,
        no_urls=True, no_emails=True, no_phone_numbers=True,
        replace_with_url="[LINK]", replace_with_email="[EMAIL]", replace_with_phone_number="[TELEFONE]"
    )
    
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = EMAIL_RESPONSE_PROMPT_TEMPLATE.format(email_text=cleaned_text)

    try:
        logger.info("Enviando requisição para a API do Google Gemini...")
        
        generation_config = genai.GenerationConfig(response_mime_type="application/json")

        response = model.generate_content(prompt, generation_config=generation_config)
        
        result_json = json.loads(response.text)
        logger.info(f"Resposta recebida do Gemini: {result_json}")

        return {
            "classification": result_json.get("classification", "Desconhecido"),
            "suggested_response": result_json.get("suggested_response", "Não foi possível gerar uma resposta.")
        }
    except Exception as e:
        logger.error(f"Erro na API do Google Gemini: {e}")
        return {"error": "Falha ao contatar a API do Gemini.", "details": str(e)}