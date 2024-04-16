from typing import Text, Dict, List

from pydantic import BaseModel


class SynthesizerConfig(BaseModel):
    db_name: Text = None
    collection_name: Text = None
    document_paths: List = None
    gen_func: Text = None
    generator: Dict = None


class EvaluatorConfig(BaseModel):
    pass


