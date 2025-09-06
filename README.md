# Servidor de Licenças

Este é um servidor de licenças simples construído com FastAPI que gera e valida códigos de ativação para aplicações cliente.

## Tecnologias Utilizadas

- Python 3.11
- FastAPI
- Uvicorn
- SQLAlchemy
- Docker

## Configuração e Instalação

1.  **Construir e Iniciar o Contêiner Docker:**

    A maneira mais simples de executar o servidor é usando o Docker. O `docker-compose.yml` irá construir a imagem e iniciar o contêiner.

    ```bash
    docker-compose up -d --build
    ```

    O servidor estará disponível em `http://localhost:8000`.

2.  **Verificar o Status do Serviço:**

    Você pode verificar se o servidor está a funcionar corretamente acedendo ao endpoint de *health check*:

    ```bash
    curl http://localhost:8000/health
    ```

    A resposta deve ser:

    ```json
    {"status":"ok"}
    ```

## Endpoints da API

### Gerar um Novo Código de Ativação (Apenas para Admin)

Para gerar um novo código de ativação para um cliente, envie uma requisição `POST` para o endpoint `/admin/generate-code`.

- **URL:** `/admin/generate-code`
- **Método:** `POST`
- **Exemplo de Requisição (cURL):**
  ```bash
  curl -X POST http://localhost:8000/admin/generate-code# licenceservertraduzai
