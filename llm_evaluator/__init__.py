import os
import llm_evaluator
from llm_evaluator.core.app_models import env_configs

APPDIR = llm_evaluator.__path__[0]
ENVFILE = os.path.join(APPDIR, "launch.json")

if not os.path.isfile(ENVFILE):
    ENVFILE = os.environ.get("env_file")
if not os.path.isfile(ENVFILE):
    raise EnvironmentError(
        "Missing env file. Please export the env file or use CLI's init"
    )
# ENVCFG = env_configs.EnvConfig(config_path=ENVFILE)
# print(ENVCFG)