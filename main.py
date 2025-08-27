import logging
import pandas as pd
import io
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware
from config import ALLOWED_ORIGINS

from services.classifier import get_email_classification

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

class EmailRequest(BaseModel):
    content: str

app = FastAPI(
    title="API de Classificação de Emails",
    description="Processa emails individualmente ou em lote via upload de CSV/Excel para classificação e sugestão de resposta com IA."
)

origins = [
    "http://localhost:3000", 
]

# 3. Adicione o middleware à sua aplicação
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/process-single-email")
async def classify_email(request: EmailRequest):
    logger.info("Endpoint /process-single-email chamado com texto.")
    email_text = request.content
    result = get_email_classification(email_text)
    logger.info("Classificação de texto concluída com sucesso.")
    return {
        "original_email": email_text,
        **result
    }

@app.post("/process-batch", summary="Processa um lote de emails de um arquivo CSV ou Excel")
async def process_batch(file: UploadFile = File(...)):
    logger.info(f"Endpoint /process-batch chamado com o arquivo: {file.filename}")
    
    if not file.filename.endswith(('.csv', '.xlsx')):
        raise HTTPException(status_code=400, detail="Formato de arquivo inválido. Por favor, envie um .csv ou .xlsx")

    try:
        contents = await file.read()
        file_stream = io.BytesIO(contents)

        if file.filename.endswith('.csv'):
            df = pd.read_csv(file_stream, quotechar='"')
        else:
            df = pd.read_excel(file_stream)
        
        if 'texto_do_email' not in df.columns:
            raise HTTPException(status_code=400, detail="O arquivo deve conter uma coluna chamada 'texto_do_email'.")

        results = []
        logger.info(f"Processando {len(df)} emails do arquivo {file.filename}...")

        for email_text in df['texto_do_email']:
            if isinstance(email_text, str) and email_text.strip():
                ai_result = get_email_classification(email_text)
                results.append({"original_email": email_text, **ai_result})
        
        
        logger.info("Processamento em lote concluído com sucesso.")
        return results

    except Exception as e:
        logger.error(f"Erro ao processar o arquivo em lote: {e}")
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro ao processar o arquivo: {e}")