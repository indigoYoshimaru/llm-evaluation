from fastapi import APIRouter, Depends
from loguru import logger

router = APIRouter(prefix="/evaluate")

@router.post("/generator")
def eval_generator(): 
    ...

@router.post("/retriever")
def eval_retriever(): 
    ...