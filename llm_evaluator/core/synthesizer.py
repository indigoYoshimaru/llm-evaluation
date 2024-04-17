from deepeval.dataset import EvaluationDataset
from deepeval.synthesizer import synthesizer
from typing import Text, Type, Any
from llm_evaluator.templates.syn_temp import CustomSynthesizeTemplate
from pydantic import BaseModel
from loguru import logger
from enum import Enum
from llm_evaluator.core.app_models.public_configs import SynthesizerConfig


class DataSource(str, Enum):
    retrieve_context = "context"
    retrieve_document_paths = "document_paths"
    retrieve_document_paths_from_folder_dir = "folder_dir"


class DatasetGenerator(BaseModel):
    config: SynthesizerConfig

    def retrieve_context(self): ...

    def retrieve_document_paths(self): ...

    def retrieve_document_paths_from_folder_dir(self): ...

    def generate(
        self,
        syn_model: Text,
        template: Type[CustomSynthesizeTemplate],
        data_source: DataSource,
    ):
        try:
            retriever = getattr(self, data_source.name)
            input_data = retriever()
        except Exception as e:
            raise e

        dataset = EvaluationDataset()
        gen_func_mapper = dict(
            context=dataset.generate_goldens,
            docs=dataset.generate_goldens_from_docs,
        )
        try:
            synthesizer.SynthesizerTemplate = template
            synthesizer = synthesizer.Synthesizer(syn_model)
            # gen_func = gen_func_mapper[self.config.]
            # gen_func(input, **self.config)
        except Exception as e:
            logger.error(f"{type(e).__name__}: {e} happened during generating dataset")
            raise e
