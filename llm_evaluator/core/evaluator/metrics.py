from deepeval.metrics import * 
from enum import Enum

class QAJudgeMetrics(Enum): 
    answer_relevancy = AnswerRelevancyMetric
    hallucination = HallucinationMetric
    faithfullness = FaithfulnessMetric
    bias = BiasMetric
    toxicity = ToxicityMetric
    

class NLPMetrics(): 
    pass 


