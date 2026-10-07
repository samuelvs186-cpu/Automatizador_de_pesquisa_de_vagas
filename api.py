from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from scraper import raspar_vagas

app = FastAPI(title="API de vagas de emprego")

class VagaSchema(BaseModel):
    titulo: str = Field(min_length=2, description="Titulo do cargo")
    empresa: str = Field(..., example="Nome da empresa", description="Nome da empresa")
    link: str = Field(description="URL para vaga")

class BuscaRequest(BaseModel):
    termo: str = Field(min_length=2, description="Tecnologiaou palavra-chave")

banco_vagas: List[VagaSchema] = []

@app.post("/buscar-vagas", response_model=List[VagaSchema])
async def buscar_vagas(request: BuscaRequest):
    try:
        dados_brutos = await raspar_vagas(request.termo)
        novas_vagas = [VagaSchema(**item) for item in dados_brutos]
        banco_vagas.extend(novas_vagas)
        return novas_vagas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar vagas: {str(e)}")

@app.get("/vagas", response_model=List[VagaSchema])
def listar_vagas():
    """Retorna todas as vagas armazenadas no banco de dados."""
    return banco_vagas    