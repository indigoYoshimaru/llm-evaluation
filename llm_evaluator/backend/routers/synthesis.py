from fastapi import APIRouter, Depends
from loguru import logger

router = APIRouter(prefix='/synthesis/')

@router.post(f'/question-answering')
def create_qa_dataset(
    
): 
    ...