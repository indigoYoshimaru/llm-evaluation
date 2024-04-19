from deepeval.dataset import EvaluationDataset
from deepeval import synthesizer
from deepeval.models import GPTModel
from typing import Text, Type, Any
from llm_evaluator.templates.syn_temp import CustomSynthesizeTemplate
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

        try:
            db_client = MongoClient(str(ENVCFG.db))
            collection = db_client[self.config.db_name][self.config.collection_name]

            doc = collection.find(dict(status="APPROVED")).sort(dict(_id=-1))[
                self.config.doc_idx
            ]

            # for chunk in doc["chunk_content"]:
            #     chunk_content.append(chunk.split("\n"))
            chunk_content = [chunk.split("\n") for chunk in doc["chunk_content"]]

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
            gen_client = GPTModel(
                model=syn_model,
                _openai_api_key=ENVCFG.openai.key,
            )
            generator = synthesizer.Synthesizer(model=gen_client)
            generator.using_native_model = True
            gen_func = gen_func_mapper[self.config.context_form]

            gen_func(generator, input_data, **self.config.generator)

        except Exception as e:
            logger.error(f"{type(e).__name__}: {e} happened during generating dataset")
            raise e
        return document_id, dataset

    def save_local(
        self,
        dataset: EvaluationDataset,
        dataset_save_dir: Text,
        document_id: Text,
    ):
        try:

            from llm_evaluator.utils.fileio import FileWriter
            import os

            file_writer = FileWriter()
            dataset_path = os.path.join(dataset_save_dir, f"{document_id}.json")
            json_data = [
                {
                    "input": golden.input,
                    "actual_output": golden.actual_output,
                    "expected_output": golden.expected_output,
                    "context": golden.context,
                }
                for golden in dataset.goldens
            ]
            file_writer.write(file_path=dataset_path, content=json_data)

        except Exception as e:
            raise e
        else:
            logger.info(f"Saved dataset to {dataset_save_dir}")
