from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase
import evaluate
from loguru import logger


class ContextRougeMetric(BaseMetric):

    def __init__(self, threshold: float = 0.5, **params):
        super().__init__()

        self.metric_type = params.get("metric_type", "rougeL")
        self.threshold = threshold
        self.async_mode = False  # does not provide async for custom metrics!

    def measure(self, test_case: LLMTestCase):
        try:
            rouge_score = evaluate.load("rouge")
            score_dict = rouge_score.compute(
                references=[[" ".join(test_case.context)]],
                predictions=[" ".join(test_case.retrieval_context)],
            )

            assert score_dict, "Empty result"

        except Exception as e:
            logger.error(f"{type(e).__name__}: {e}")
            raise e
        else:
            logger.success(
                f"ROUGE score comparison for {test_case.input} results {score_dict}"
            )
            
            self.score = round(score_dict.get(self.metric_type, 0), 3)
            self.success = True
            self.reason = ""
            if self.score < self.threshold:
                self.success = False
                self.reason = "Score below threshold"

    def is_successful(self):
        return self.success

    @property
    def __name__(self):
        return "ROUGE"


class ContextBleuMetric(BaseMetric):

    def __init__(self, threshold: float = 0.5, **params):
        super().__init__()
        self.threshold = threshold
        self.async_mode = False  # does not provide async for custom metrics!

    def measure(self, test_case: LLMTestCase):
        try:
            bleu_score = evaluate.load("bleu")
            score_dict = bleu_score.compute(
                references=[[" ".join(test_case.context)]],
                predictions=[" ".join(test_case.retrieval_context)],
            )

            assert score_dict, "Empty result"

        except Exception as e:
            logger.error(f"{type(e).__name__}: {e}")
            raise e
        else:
            logger.success(
                f"BLEU score comparison for {test_case.input} results {score_dict}"
            )
            self.score = round(score_dict.get("bleu", 0), 3)
            self.success = True
            self.reason = ""
            if self.score < self.threshold:
                self.success = False
                self.reason = "Score below threshold"

    def is_successful(self):
        return self.success

    @property
    def __name__(self):
        return "BLEU"
