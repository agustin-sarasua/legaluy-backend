import os
import uvicorn

print("Loading .env file")
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())  # read local .env file

from app.domain.usecases.process_chat_msg import ProcessChatMsgUseCase
from app.domain.usecases.search_bjn_usecase import SearchBJNUseCase
from fastapi.middleware.cors import CORSMiddleware

from app.presentation.routers import search_router, chat_router

from fastapi import FastAPI, Form


search_router.search_use_case = SearchBJNUseCase()
chat_router.process_msg_use_case = ProcessChatMsgUseCase()

app = FastAPI()

app.include_router(search_router.search_router)
app.include_router(chat_router.chat_router)

origins = [
    "http://localhost",
    "http://localhost:4200",
    # "https://c761-2003-e9-5f11-3bb5-a0df-4cff-f063-9692.ngrok-free.app",
    "https://www.reservamedirecto.com",
    "https://reservamedirecto.com"
    # Add more origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz")
async def root():
    return "OK"


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
