from pydantic import BaseModel

class CodeCreate(BaseModel):
    pass # Não precisa de input para criar, será aleatório

class CodeVerify(BaseModel):
    activation_code: str

class CodeResponse(BaseModel):
    code: str
    is_used: bool

    class Config:
        orm_mode = True

class VerifyResponse(BaseModel):
    status: str
    client_key: str | None = None
    message: str