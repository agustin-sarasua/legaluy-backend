import logging
import os
from fastapi import FastAPI, Form, Depends

import traceback


from fastapi import APIRouter
from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse

from app.domain.entities import BusinessException
from app.domain.entities.entities import Conversation, SearchRequest
from app.domain.usecases import SearchBJNUseCase
from app.domain.usecases.process_chat_msg import ProcessChatMsgUseCase

logger = logging.getLogger(__name__)
chat_router = APIRouter()

process_msg_use_case: ProcessChatMsgUseCase


@chat_router.post("/message")
async def chat_message(
    conversaion: Conversation,
    usecase: ProcessChatMsgUseCase = Depends(lambda: process_msg_use_case),
):
    try:
        result = usecase.execute(conversaion)
        return JSONResponse(content=result, status_code=200)
    except BusinessException as e:
        traceback.print_exc()
        return JSONResponse(content=str(e.detail), status_code=400)
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Exception {str(e)}")
        return JSONResponse(content=str(e), status_code=500)


# Define the `routes` attribute as a list containing the reservation_router instance
routes = [chat_router]
