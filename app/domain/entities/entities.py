from typing import List, Any, Optional
# from app.model import Conversation
from datetime import datetime
from pydantic import BaseModel


class SearchRequest(BaseModel):
    text: str = None
    

class SearchResponse(BaseModel):
    hits: int
    total_hits: int
    results: List[Any]


class SentenciaModel(BaseModel):
    materias: Optional[List[List[str]]]
    firmantes: Optional[List[List[str]]]
    redactores: Optional[List[List[str]]]
    abstract: Optional[List[List[str]]]
    descriptores: Optional[List[List[str]]]
    resumen: Optional[List[List[str]]]
    sentencia: Optional[str]
    numero: Optional[str]
    sede: Optional[str]
    importancia: Optional[str]
    tipo: Optional[str]
    fecha: Optional[str]
    ficha: Optional[str]
    procedimiento: Optional[str]

class Message(BaseModel):
    role: str
    text: str

class Conversation(BaseModel):
    messages: List[Message]
    sentencia_model: SentenciaModel = None


