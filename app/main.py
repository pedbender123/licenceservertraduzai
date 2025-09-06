from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import secrets
import string
from datetime import datetime

from . import models, schemas
from .database import SessionLocal, engine, Base

# Cria as tabelas no banco de dados na primeira inicialização
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Função para obter uma sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_activation_code():
    """Gera um código de ativação numérico de 6 dígitos."""
    return ''.join(secrets.choice(string.digits) for i in range(6))

@app.post("/admin/generate-code", response_model=schemas.CodeResponse)
def create_activation_code(db: Session = Depends(get_db)):
    """
    [ADMIN] Endpoint para gerar um novo código de ativação para um cliente.
    """
    new_code_str = generate_activation_code()
    # Garante que o código é único
    while db.query(models.ActivationCode).filter(models.ActivationCode.code == new_code_str).first():
        new_code_str = generate_activation_code()

    db_code = models.ActivationCode(code=new_code_str)
    db.add(db_code)
    db.commit()
    db.refresh(db_code)
    return db_code

@app.post("/verify-code", response_model=schemas.VerifyResponse)
def verify_code(request: schemas.CodeVerify, db: Session = Depends(get_db)):
    """
    [CLIENTE] Endpoint que a aplicação do cliente usará para validar um código.
    """
    code_to_verify = request.activation_code
    db_code = db.query(models.ActivationCode).filter(models.ActivationCode.code == code_to_verify).first()

    if not db_code:
        raise HTTPException(status_code=404, detail="Código de ativação inválido.")

    if db_code.is_used:
        raise HTTPException(status_code=400, detail="Este código de ativação já foi utilizado.")

    # Se o código é válido e não foi usado, marca como usado e gera a chave do cliente
    db_code.is_used = True
    db_code.activated_at = datetime.utcnow()
    # Gera uma chave única e permanente para esta instalação de cliente
    client_key = secrets.token_hex(32)
    db_code.client_key = client_key

    db.commit()

    return schemas.VerifyResponse(
        status="success",
        client_key=client_key,
        message="Aplicação ativada com sucesso."
    )

@app.get("/health")
def health_check():
    return {"status": "ok"}