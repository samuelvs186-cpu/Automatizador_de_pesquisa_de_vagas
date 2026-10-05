from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from scraper import raspar_vagas

app = FastAPI(title="API de vagas de emprego")

class VagaSchema(BaseModel):
    titulo: str = Field(min_length=2, description="Titulo do cargo")
    empresa: str = Field(..., example="Nome da empresa", description="Nome da empresa")
    link: str = Field(description="URL para vaga")

class BuscaRequest(BaselModel):
    termo: str = Field(min_length=2, description="Tecnologiaou palavra-chave")