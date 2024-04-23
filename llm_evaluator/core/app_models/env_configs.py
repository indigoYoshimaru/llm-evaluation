from pydantic import BaseModel
from typing import Text, Dict
from loguru import logger
from llm_evaluator.utils import fileio, secrets
from enum import Enum


class Database(BaseModel):
    address: Text
    auth: Text
    password: Text
    user: Text

    def __str__(self) -> Text:
        # temporary only works with mongo!
        if self.address.startswith("mongodb"):
            return (
                "mongodb://{user}:{password}@{address}/?authSource={auth}".format(
                    **self.model_dump()
                )
                .replace("?replicaSet=rs/", "")
                .replace("@mongodb://", "@")
            )
        return ""


class Client(BaseModel):
    host: Text
    authorization: Text


class ChatAPI(BaseModel):
    key: Text


class EnvVarEnum(str, Enum):
    db = "database"
    sv = "service"


class EnvConfig:

    def __init__(self, config_path: Text):
        file_reader = fileio.FileReader()
        try:
            cfg_dict = file_reader.read(config_path)["env"]
            cfg_dict = secrets.decode(cfg_dict)
        except Exception as e:
            logger.warning(
                f"{type(e).__name__}: {e}. Cannot read config {config_path}."
            )
            try:
                from llm_evaluator import APPDIR

                config_path = config_path.replace(APPDIR, "")
                logger.warning(f"Retrying with relative path {config_path}")
                cfg_dict = file_reader.read(config_path)["env"]
                cfg_dict = secrets.decode(cfg_dict)
            except Exception as e:
                raise FileNotFoundError(
                    f"Are you sure your both config file and the path {config_path} are correct?"
                )
        else:
            del file_reader
            logger.info(f"Mapping the configs")

        try:
            for db_name, db_val in cfg_dict["database"].items():
                self.__dict__[db_name] = Database(**db_val)
            for sv_name, sv_dict in cfg_dict["service"].items():
                if "client" in sv_name:
                    service = Client(**sv_dict)
                elif sv_name in ["openai", "claude"]:
                    service = ChatAPI(**sv_dict)
                else:
                    service = sv_dict
                self.__dict__[sv_name] = service
        except Exception as e:
            raise RuntimeError(
                "Cannot mapping your Env config. You can start yelling now"
            )
        else:
            logger.info(f"Config mapped!")
