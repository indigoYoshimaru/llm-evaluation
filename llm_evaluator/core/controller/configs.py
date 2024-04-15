from typing import Text, Dict, List

from pydantic import BaseModel 

class SynthesizerConfig(BaseModel): 
    pass

class EvaluatorConfig(BaseModel): 
    metric_params

class Config(BaseModel): 
    pass

