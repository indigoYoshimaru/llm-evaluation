from deepeval.metrics import *
from llm_evaluator.core.metrics.custom_metrics import *
from enum import Enum
from pydantic import BaseModel


class QAJudgeMetrics(Enum):
    answer_relevancy = AnswerRelevancyMetric
    hallucination = HallucinationMetric
    faithfullness = FaithfulnessMetric
    bias = BiasMetric
    toxicity = ToxicityMetric


class RAGJudgeMetrics(Enum):
    context_rouge = ContextRougeMetric
    context_bleu = ContextBleuMetric
    contextual_precision = ContextualPrecisionMetric
    contextual_recall = ContextualRecallMetric
    contextual_relevancy = ContextualRelevancyMetric

class MQCJudgeMetrics(Enum):
    pass


class MetricTypeEnum(BaseModel): 
    mqc: Enum = MQCJudgeMetrics
    qa: Enum = QAJudgeMetrics
    rag: Enum = RAGJudgeMetrics



