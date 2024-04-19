from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase
import evaluate


class ContextRougeMetric(BaseMetric):

    def __init__(self, threshold: float = 0.5):
        self.threshold = threshold
        self.rouge = evaluate.load("rogue")

    def measure(self, test_case: LLMTestCase):
        self.score = self.rouge.compute(
            references=test_case.context, predictions=test_case.retrieval_context
        )
        self.success = True
        if self.score < self.threshold:
            self.success = False

        return self.score

    def is_successful(self):
        return self.success

    @property
    def __name__(self):
        return "ROUGE"


class ContextBleuMetric(BaseMetric):

    def __init__(self, threshold: float = 0.5):
        self.threshold = threshold
        self.bleu = evaluate.load("bleu")

    def measure(self, test_case: LLMTestCase):
        self.score = self.bleu.compute(
            references=test_case.context, predictions=test_case.retrieval_context
        )
        self.success = True
        if self.score < self.threshold:
            self.success = False

        return self.score

    def is_successful(self):
        return self.success

    @property
    def __name__(self):
        return "ROUGE"
