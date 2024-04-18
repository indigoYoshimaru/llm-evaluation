from pydantic import BaseModel
from deepeval import evaluate
from typing import List

class Evaluator(BaseModel): 
    metrics: List
    threshold: float

    def eval_task(self, metrics): 
        

    def eval_gen_model(self, metrics): 
        ...

    def __get_answer(self, input): 
        ...
        # mostly use to evaluate RAG 


    def __get_answer(self, input, context): 
        # get answer with provided context
        ...
        # invoke chat api 


