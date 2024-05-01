from fastapi import APIRouter, Depends
from loguru import logger

router = APIRouter()


@router.get("/health")
def health():
    return dict(msg="App running")


@router.get("/")
def main():
    msg = f"Main route is not implemented, please temperarily use /docs for API UI"
    return msg
