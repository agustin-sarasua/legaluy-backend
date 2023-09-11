import logging
import os
from fastapi import FastAPI, Form, Depends

import traceback


from fastapi import APIRouter
from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse

from app.domain.entities import BusinessException
from app.domain.entities.entities import SearchRequest
from app.domain.usecases import SearchBJNUseCase

logger = logging.getLogger(__name__)
search_router = APIRouter()

search_use_case: SearchBJNUseCase


@search_router.post("/search")
async def search_bjn(
    search_request: SearchRequest,
    usecase: SearchBJNUseCase = Depends(lambda: search_use_case),
):
    try:
        result = usecase.execute(search_request)
        return JSONResponse(content=result.model_dump(), status_code=200)
    except BusinessException as e:
        traceback.print_exc()
        return JSONResponse(content=str(e.detail), status_code=400)
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Exception {str(e)}")
        return JSONResponse(content=str(e), status_code=500)


# Define the `routes` attribute as a list containing the reservation_router instance
routes = [search_router]
