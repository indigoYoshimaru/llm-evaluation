from deepeval.metrics import * 
from pydantic import BaseModel

class JudgeMetrics(BaseModel): 
    pass

class NLPMetrics(BaseModel): 
    pass 

# and class of metrics that inheirits deepeval metrics