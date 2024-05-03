from pydantic import BaseModel, NonNegativeInt
from typing import Text, List, Dict
from gunicorn.app.wsgiapp import WSGIApplication
from loguru import logger


class StandaloneApplication(WSGIApplication):
    def __init__(self, app_uri: Text, options: Dict = None):
        self.options = options
        self.app_uri = app_uri
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)


class WebServerConfigs(BaseModel):
    bind: Text
    worker_class: Text
    workers: NonNegativeInt


class APIConfigs(BaseModel):
    web_server: WebServerConfigs
    api_info: Dict

    def __init__(self, config_path: Text, num_workers: NonNegativeInt):
        try:
            from llm_evaluator.utils.fileio import FileReader

            assert config_path, "Empty config path"
            config_dict = FileReader().read(config_path)
            web_server_cfg = config_dict["web_server"]

            web_server = WebServerConfigs(
                bind=f"{web_server_cfg.pop('host')}:{web_server_cfg.pop('port')}",
                workers=num_workers,
                **web_server_cfg,
            )
        except Exception as e:
            logger.error(f"{type(e).__name__}: {e} happened while loading app configs")
            raise e

        else:
            logger.success(f"Config loaded from {config_path}")
            super().__init__(
                web_server=web_server,
                api_info=config_dict["api_info"],
            )
