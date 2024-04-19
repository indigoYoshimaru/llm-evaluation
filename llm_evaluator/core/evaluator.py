from pydantic import BaseModel
from deepeval import evaluate
from deepeval.dataset import EvaluationDataset
from typing import List, Text
from llm_evaluator.core.app_models.public_configs import EvaluatorConfig
from loguru import logger
from llm_evaluator import ENVCFG
import asyncio


class Evaluator(BaseModel):
    metrics: List = None
    config: EvaluatorConfig = None
    dataset: EvaluationDataset = None

    

    def eval_rag(self, dataset_path: Text): ...

    def eval_gen_model(self, dataset_path: Text, judge_model: Text):
        try: 
            self.dataset = EvaluationDataset()
            self.dataset.add_test_cases_from_json_file(
                file_path=dataset_path,
                input_key_name="input",
                actual_output_key_name="actual_output",
                expected_output_key_name="expected_output",
                context_key_name="context",
            )

            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.__invoke_chat_api())
            loop.close()
        except Exception as e: 
            logger.error(f'{type(e).__name__}: {e}. Error during invoking API.')
            raise e
        
        try: 
            metric_params = dict(
                threshold = self.config.threshold, 
                model = judge_model, 
            )
        except Exception as e: 
            raise e
        
        return test_results


    async def __invoke_chat_api(self):
        import requests as re

        task_list = list()
        try:
            
            for idx, test_case in enumerate(self.dataset.test_cases):
                response = re.post(
                    url=self.config.model_api,
                    headers=ENVCFG.headers,
                    json=dict(question=test_case.input),
                ).json()

                response_data = response.get("data", [])
                assert response_data, "Invalid request"
                ticket_id = response_data[0].get("ticket_id", "")
                assert ticket_id, "No ticket id"
                # answer, context = self.__get_answer(ticket_id=ticket_id)

                task_list.append(
                    asyncio.create_task(
                        self.__get_answer(test_case_idx=idx, ticket_id=ticket_id)
                    )
                )
                if len(task_list)>=3: 
                    await asyncio.wait(task_list)
                    task_list = list()

            await asyncio.wait(task_list)
        except Exception as e:
            logger.error(f"{type(e).__name__}: {e}. Cannot invoke chat api")
            raise e

    async def __get_answer(self, test_case_idx: int, ticket_id: int):
        from pymongo import MongoClient

        try:

            db_client = MongoClient(str(ENVCFG.db))
            collection = db_client[self.config.db_name][self.config.collection_name]
        except Exception as e:
            logger.error(f"{type(e).__name__}: {e}. Cannot connect to MongoDB")
            raise e

        try:

            chat_ticket = collection.find(dict(ticket_id=ticket_id))[0]
            print(chat_ticket)
            while chat_ticket["status"] != "DONE":
                await asyncio.sleep(2)
                chat_ticket = collection.find(dict(ticket_id=ticket_id))[0]

            self.dataset.test_cases[test_case_idx].actual_output = chat_ticket["answer"]
            self.dataset.test_cases[test_case_idx].retrieval_context = [
                chunk["page_content"] for chunk in chat_ticket["context"]
            ]
            print(self.dataset.test_cases[test_case_idx])
        except Exception as e:
            raise e
