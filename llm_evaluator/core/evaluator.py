import asyncio
from loguru import logger
from typing import List, Text
from pydantic import BaseModel
from deepeval import evaluate
from deepeval.dataset import EvaluationDataset
from llm_evaluator import ENVCFG
from llm_evaluator.core.metrics import (
    MetricTypeEnum,
    ContextRougeMetric,
    ContextBleuMetric,
)
from llm_evaluator.core.app_models.public_configs import EvaluatorConfig
from llm_evaluator.core.visual import view_result


class Evaluator(BaseModel):
    metrics: List = None
    config: EvaluatorConfig = None
    dataset: EvaluationDataset = None

    def __init__(self, config: EvaluatorConfig, question_type: Text, judge_model: Text):
        try:
            metric_type = MetricTypeEnum().model_dump()[question_type]
            metrics = [
                getattr(metric_type, metric_name).value(
                    **config.metric_params, model=judge_model
                )
                for metric_name in config.metrics
                if config.metrics[metric_name]
            ]

        except Exception as e:
            raise e
        else:
            super().__init__(metrics=metrics, config=config)

    def evaluate(self, dataset_path: Text):
        try:
            self.dataset = EvaluationDataset()
            self.dataset.add_test_cases_from_json_file(
                file_path=dataset_path,
                input_key_name="input",
                actual_output_key_name="actual_output",
                expected_output_key_name="expected_output",
                context_key_name="context",
            )
            logger.info(f"Invoking chat API...")
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.__invoke_chat_api())
            loop.close()
        except Exception as e:
            logger.error(f"{type(e).__name__}: {e}. Error during invoking API.")
            raise e
        else:
            logger.success(f"Chat API invoked!")

        try:
            run_async = True
            for metric in self.metrics:
                if isinstance(metric, ContextBleuMetric) or isinstance(
                    metric, ContextRougeMetric
                ):
                    run_async = False

            logger.info("Running evaluation...")
            test_results = evaluate(
                metrics=self.metrics,
                test_cases=self.dataset.test_cases,
                use_cache=False,
                print_results=False,
                write_cache=False,
                show_indicator=False,
                run_async=run_async,
            )

        except Exception as e:
            raise e
        else:
            view_result(result=test_results)
            return test_results

    async def __invoke_chat_api(self):
        import requests as re

        task_list = list()

        for idx, test_case in enumerate(self.dataset.test_cases):
            try:
                response = re.post(
                    url=self.config.model_api,
                    headers=ENVCFG.headers,
                    json=dict(
                        question=test_case.input,
                        conversation_id=ENVCFG.conversation_id,
                    ),
                    timeout=20,
                ).json()

                response_data = response.get("data", [])
                assert response_data, response
                ticket_id = response_data[0].get("ticket_id", "")
                assert ticket_id, "No ticket id"

            except re.exceptions.Timeout as timeout_err:
                logger.warning(
                    f"{type(timeout_err).__name__}: {timeout_err} happened for {test_case.input}. Skipping..."
                )
                continue
            except AssertionError as e:
                logger.warning(f"Empty response for question {test_case.input=}")
                continue
            try:

                task_list.append(
                    asyncio.create_task(
                        self.__get_answer(test_case_idx=idx, ticket_id=ticket_id)
                    )
                )
                if len(task_list) >= 3:
                    await asyncio.wait(task_list)
                    task_list = list()
            except Exception as e:
                logger.error(f"{type(e).__name__}: {e} Cannot get answer from chat API")
                continue
        if len(task_list) > 0:
            await asyncio.wait(task_list)

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

            while chat_ticket["status"] != "DONE":
                await asyncio.sleep(3)
                chat_ticket = collection.find(dict(ticket_id=ticket_id))[0]
                logger.info(f"Getting answers from {ticket_id=}")

            self.dataset.test_cases[test_case_idx].actual_output = chat_ticket["answer"]
            context_chunks = chat_ticket["context"]
            assert context_chunks, "No context retrieved!"
            logger.success(f"Got answers from {ticket_id=}!")
            score_max_arg = max(
                range(len(context_chunks)), key=lambda x: context_chunks[x]["score"]
            )

        except Exception as e:
            logger.error(
                f"{type(e).__name__}: {e}. Cannot retrieve content of ticket {ticket_id}"
            )
            self.dataset.test_cases[test_case_idx].retrieval_context = [
                "No context retrieved"
            ]
        else:

            self.dataset.test_cases[test_case_idx].retrieval_context = [
                context_chunks[score_max_arg]["page_content"]
            ]
