from deepeval.dataset import EvaluationDataset
from deepeval.synthesizer import Synthesizer
from deepeval.synthesizer import synthesizer
from llm_evaluator.templates import syn_temp
from pydantic import BaseModel

class DatasetGenerator(BaseModel): 
    ...