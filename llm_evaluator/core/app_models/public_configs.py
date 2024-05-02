from typing import Text, Dict, List
from pydantic import BaseModel
from llm_evaluator.utils.fileio import FileReader
from loguru import logger

file_reader = FileReader()


class SynthesizerConfig(BaseModel):
    db_name: Text = None
    collection_name: Text = None
    document_paths: List = None
    generator: Dict = None
    context_form: Text = None
    doc_idx: int = 0

    def __init__(
        self,
        config_path: Text,
        data_source: Text,
        cfg_dict: Dict = None,
    ):
        try:
            if cfg_dict:
                super().__init__(context_form=data_source, **cfg_dict)
                return
            cfg_dict = file_reader.read(config_path)
            assert cfg_dict, "Cannot find config file"

        except Exception as e:
            raise e

        try:
            cfg_dict_opt = cfg_dict.get(data_source, {})
            assert cfg_dict_opt, "Generating from docs"
            context_form = data_source
        except AssertionError as e:
            logger.warning(f"{e}")
            context_form = "docs"
            cfg_dict_opt = cfg_dict.get(context_form)
        finally:
            logger.info(f"Retrieved synthesizer configs {cfg_dict_opt}")
        super().__init__(context_form=context_form, **cfg_dict_opt)


class EvaluatorConfig(BaseModel):
    db_name: Text = None
    collection_name: Text = None
    metrics: Dict = None
    model_api: Text = None
    metric_params: Dict = None

    def __init__(self, config_path: Text):
        try:
            if cfg_dict:
                super().__init__(**cfg_dict)
                return
            cfg_dict = file_reader.read(config_path)
            assert cfg_dict, "Cannot find config file"
        except Exception as e:
            raise e
        else:
            super().__init__(**cfg_dict)
