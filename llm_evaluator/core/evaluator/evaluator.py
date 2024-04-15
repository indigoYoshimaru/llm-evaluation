from pydantic import BaseModel

class Evaluator(BaseModel): 

    def eval_task(self, metrics, ): 
        ...

    def eval_gen_model(self, metrics): 
        ...

    def __get_answer(self, input): 
        ...
        # mostly use to evaluate RAG 


    def __get_answer(self, input, context): 
        # get answer with provided context
        ...
        # invoke chat api 


