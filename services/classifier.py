import os
import logging
import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
if not API_TOKEN:
    raise ValueError("Chave da API da Hugging Face não encontrada. Verifique seu arquivo .env")

MODEL_NAME = "facebook/bart-large-mnli"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

def get_email_classification(email_text: str) -> dict:

    if not email_text or not isinstance(email_text, str) or not email_text.strip():
        return {"error": "Texto do email inválido ou vazio."}
    
    original_length = len(email_text)
    if original_length > 3000:
        email_text = email_text[:3000]
        logger.warning(f"Texto truncado de {original_length} para 3000 caracteres")

        
    payload = {
        "inputs": email_text,
        "parameters" : {
            "candidate_labels": ["Produtivo", "Improdutivo"]
        },
        "options": {
            "wait_for_model": True
        }
    }

    try:
        logger.info("Enviando requisição para a API da Hugging Face...")
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        result = response.json()
        logger.info("Resposta da API recebida com sucesso.")

        top_score_index = result["scores"].index(max(result["scores"]))
        classification = result["labels"][top_score_index]

        suggested_response = "Resposta padrão."
        if classification == "Produtivo":
            suggested_response = "Obrigado pelo seu email. Estamos analisando e retornaremos em breve."
        elif classification == "Improdutivo":
            suggested_response = "Agradecemos a mensagem. Arquivaremos para referência."

        return {"classification": classification, "suggested_response": suggested_response}
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Falha na comunicação com a API de IA: {e}")
        return {"error": "Falha ao contatar a API de IA.", "details": str(e)}
    
    except (KeyError, IndexError) as e:
        logger.error(f"Resposta inesperada da API de IA: {e}")
        return {"error": "Resposta inválida da API de IA.", "details": str(e), "raw_response": result if 'result' in locals() else 'N/A'}