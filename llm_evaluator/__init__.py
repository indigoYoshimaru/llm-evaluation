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
        logger.error(f"{type(e).__name__}: {e}. Environment file missing")
        raise e
    else:
        logger.info(f"Loading env config from {ENVFILE}")
        ENVCFG = env_configs.EnvConfig(config_path=ENVFILE)
        os.environ["OPENAI_API_KEY"] = ENVCFG.openai.key


def trigger_init():
    import dotenv

    global ENVCFG
    try:
        dotenv.load_dotenv(dotenv_path=os.path.join(APPDIR, ".env"))
        default_init = os.environ.get("default_run", False)
        assert default_init, "Cannot run default init, Please use CLI's init!"
        logger.info(f"{ENVCFG=}")
        init()
    except Exception as e:
        logger.warning(f"{type(e).__name__}: {e}")



trigger_init()
