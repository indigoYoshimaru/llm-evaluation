import os

from fastapi import FastAPI
from llm_evaluator.backend.routers import get_all_routers
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from llm_evaluator import trigger_init

try:
    trigger_init()

    app = FastAPI(
        title="LLM Evaluator",
        description="Fast synthesis dataset creation and LLM pipeline evaluation. Accelerate testing and performance assessment with ease.",
        version="0.0.1",
        docs_url="/docs",
        root_path=os.getenv("ROOT_PATH", ""),
    )

    # app.mount("/frontend", StaticFiles(directory ="frontend", html=True), name = "frontend" )

    origins = ["http://0.0.0.0:8000"]
    # app.add_middleware(
    #     CORSMiddleware,
    #     allow_origins=origins,
    #     allow_credentials=True,
    #     allow_methods=["*"],
    #     allow_headers=["*"],
    # )

    for router in get_all_routers():
        app.include_router(router)

    logger.info(f"Starting app...")

except Exception as e:
    msg = f"Cannot start app due to error {type(e).__name__}: {e}"
    logger.error(msg)
    raise RuntimeError(msg)
