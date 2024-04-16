from deepeval.dataset import EvaluationDataset
from deepeval.synthesizer import Synthesizer
from deepeval.synthesizer import synthesizer
from typing import Text, Type, Any
from llm_evaluator.templates.syn_temp import CustomSynthesizeTemplate
from pydantic import BaseModel
from loguru import logger
from enum import Enum


class DataSource(str, Enum):
    retrieve_context = "context"
    retrieve_document_paths= "document_paths"
    retrieve_document_paths_from_folder_dir = "folder_dir"


class DatasetGenerator(BaseModel):
    config: Any

    def retrieve_context(self): ...

    def retrieve_document_paths(self): ...

    def retrieve_document_paths_from_folder_dir(self): ...

    def generate(
        self,
        syn_model: Text,
        template: Type[CustomSynthesizeTemplate],
        data_source: DataSource,
    ):
        retriever = getattr(self, data_source.name)
        logger.info(f'{retriever=}')
        input_data = retriever()
        try:
            synthesizer.SynthesizerTemplate = template
            synthesizer = Synthesizer(syn_model)
            dataset = EvaluationDataset()
            gen_func = getattr(dataset, self.config.gen_func)
            gen_func(input, **self.config)
        except Exception as e:
            logger.error(f"{type(e).__name__}: {e} happened during generating dataset")
            raise e
