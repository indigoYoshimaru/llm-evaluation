import os

from fastapi import FastAPI
from llm_evaluator.api.routers import get_all_routers
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

# from llm_evaluator import trigger_init

try:

    from llm_evaluator import APICFG

    app = FastAPI(**APICFG.api_info)

    # app.mount("/frontend", StaticFiles(directory ="frontend", html=True), name = "frontend" )

    # origins = api_cfg.origins
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
