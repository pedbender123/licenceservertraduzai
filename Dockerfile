FROM python:3.11-slim-bookworm

WORKDIR /app

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app/app

# Expõe a porta que a API irá rodar
EXPOSE 8000

# Comando para iniciar a API com Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]