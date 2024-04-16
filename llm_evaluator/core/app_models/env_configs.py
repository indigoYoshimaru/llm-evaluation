from pydantic import BaseModel
from typing import Text
from loguru import logger
from llm_evaluator.utils import fileio, secrets


class Database(BaseModel):
    address: Text
    auth: Text
    password: Text
    user: Text

    def __str__(self) -> Text:
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


class EnvConfig(BaseModel):
    # 
    def __init__(self, config_path: Text):
        super().__init__()
        try:
            file_reader = fileio.FileReader()
            cfg_dict = file_reader.read(config_path)['env']
            cfg_dict = secrets.decode(cfg_dict)
            del file_reader
            for db_name, db_val in cfg_dict['database'].items(): 
                setattr(self, db_name, Database(**db_val))
        except Exception as e:
            raise e
