import os
import llm_evaluator
from llm_evaluator.core.app_models import env_configs
from loguru import logger

APPDIR = llm_evaluator.__path__[0]
ENVFILE = os.path.join(APPDIR, "launch.json")

try:
    if not os.path.exists(ENVFILE):
        ENVFILE = os.environ.get("env_file")
    assert ENVFILE, "Envfile path not exported."
    assert os.path.exists(ENVFILE), "Invalid envfile path provided."
    assert os.path.isfile(ENVFILE), "Invalid envfile."
    
except Exception as e:
    logger.error(f"{type(e).__name__}: {e}. Missing env file. Please export the env file or use CLI's init")
else:
    logger.info(f"Loading env config from {ENVFILE}")
    ENVCFG = env_configs.EnvConfig(config_path=ENVFILE)
    os.environ["OPENAI_API_KEY"] = ENVCFG.openai.key
