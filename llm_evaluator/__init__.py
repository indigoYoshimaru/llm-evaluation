import os
import llm_evaluator
from llm_evaluator.core.app_models import env_configs
from loguru import logger

APPDIR = llm_evaluator.__path__[0]
ENVFILE = os.path.join(APPDIR, "launch.json")
ENVCFG = None

def init():
    global APPDIR, ENVFILE, ENVCFG
    try:
        if not os.path.exists(ENVFILE):
            ENVFILE = os.environ.get("env_file")
            logger.info(f"Retrieving env file from {ENVFILE}")
        assert ENVFILE, "Envfile path not exported."
        assert os.path.exists(ENVFILE), "Invalid envfile path provided."
        assert os.path.isfile(ENVFILE), "Invalid envfile."

    except Exception as e:
        logger.error(
            f"{type(e).__name__}: {e}. Missing env file. Please export the env file or use CLI's init"
        )
        raise e
    else:
        os.environ["default_run"] = "True"
        logger.info(f"Loading env config from {ENVFILE}")
        ENVCFG = env_configs.EnvConfig(config_path=ENVFILE)
        os.environ["OPENAI_API_KEY"] = ENVCFG.openai.key


if __name__ == "__main__":
    if os.environ["default_init"]:
        init()
    else:
        logger.info(f"Please export the env file to env_file or use CLI's init")
