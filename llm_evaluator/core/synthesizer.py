from deepeval.dataset import EvaluationDataset
from deepeval import synthesizer
from deepeval.models import GPTModel
from deepeval.progress_context import synthesizer_progress_context
from typing import Text, Type, Any
from llm_evaluator.templates.syn_temp import (
    CustomSynthesizeTemplate,
    VietnamEvolutionTemplate,
)
from pydantic import BaseModel
from loguru import logger
from llm_evaluator.core.app_models.public_configs import SynthesizerConfig
from llm_evaluator import ENVCFG
from llm_evaluator.core.enums import DataSourceEnum


class Synthesizer(BaseModel):
    config: SynthesizerConfig

    def retrieve_context(self):
        # temporary works for Mongo only!
        from markdownify import markdownify as md
        from pymongo.mongo_client import MongoClient

        global ENVCFG
        try:
            db_client = MongoClient(str(ENVCFG.db))
            collection = db_client[self.config.db_name][self.config.collection_name]

            doc = collection.find(
                dict(status="APPROVED", document_id=self.config.doc_idx)
            )[0]
            assert doc, "No document found"
            chunk_content = [chunk.split("\n") for chunk in doc["chunk_content"]]
            chunk_content = [
                list(filter(lambda x: x and not x.isspace(), chunk))
                for chunk in chunk_content
            ]
            logger.info(f"Retrieved {len(chunk_content)} chunks for this document")
        except Exception as e:
            raise e
        else:
            return doc["document_id"], chunk_content

    def retrieve_document_paths(self):
        return self.config.document_paths

    def retrieve_document_paths_from_folder_dir(self):
        try:
            import os

            document_paths = [
                os.path.join(self.document_dir, fname)
                for fname in os.listdir(os.path.join(self.document_dir))
            ]
        except Exception as e:
            raise e
        else:
            return document_paths

    def generate(
        self,
        syn_model: Text,
        template: Type[CustomSynthesizeTemplate],
        data_source: DataSourceEnum,
    ):
        try:
            retriever = getattr(self, data_source.name)
            document_id, input_data = retriever()
            logger.info(f"{input_data=}")
        except Exception as e:
            raise e
        else:
            logger.success(f"Data retrieved from {data_source.name}")

        dataset = EvaluationDataset()
        gen_func_mapper = dict(
            context=dataset.generate_goldens,
            docs=dataset.generate_goldens_from_docs,
        )
        try:
            synthesizer.synthesizer.SynthesizerTemplate = template
            synthesizer.synthesizer.EvolutionTemplate = VietnamEvolutionTemplate

            # gen_client = GPTModel(
            #     model=syn_model,
            #     _openai_api_key=ENVCFG.openai.key,
            # )
            generator = synthesizer.Synthesizer(model=syn_model)
            generator.using_native_model = True
            gen_func = gen_func_mapper[self.config.context_form]
            logger.info(f"Start generating dataset. This may take a few minutes... ")
            gen_func(
                generator,
                input_data,
                **self.config.generator,
                _show_indicator=False,
            )
            processed_dataset = self._post_process(dataset)
        except Exception as e:
            logger.error(f"{type(e).__name__}: {e} happened during generating dataset")
            raise e
        else:
            logger.success(
                f"Generated for document number {document_id} in the database"
            )
            return document_id, processed_dataset

    def _post_process(self, dataset: EvaluationDataset):
        return [
            {
                "input": golden.input,
                "actual_output": golden.actual_output,
                "expected_output": golden.expected_output,
                "context": golden.context,
            }
            for golden in dataset.goldens
        ]
