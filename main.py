import logging
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

from services.classifier import get_email_classification

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger= logging.getLogger(__name__)

class EmailRequest(BaseModel):
    content: str

app = FastAPI()

@app.get("/")
async def root():
    return{"message": "Hello World"}

@app.post("/classify")
async def classify_email(request: EmailRequest):
    logger.info("Endpoint /classify chamado com texto.")

    email_text = request.content
     
    result = get_email_classification(email_text)

    return {
        "received_text": email_text,
        **result
    }

@app.post("/classify/file")
async def classify_email_from_file(file: UploadFile = File(...)):
    logger.info(f"Endpoint /classify/file chamado com o arquivo: {file.filename}")
    
    try:
        contents = await file.read()
        email_text = contents.decode("utf-8")
    except Exception as e:
        return {"error": "Houve um erro ao ler o arquivo. Verifique se ele é um arquivo de texto (.txt) válido.", "details": str(e)}
    finally:
        await file.close()
    
    result = get_email_classification(email_text)
    
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        **result
    }

