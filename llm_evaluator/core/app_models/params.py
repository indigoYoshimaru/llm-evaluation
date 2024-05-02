from pydantic import BaseModel, NonNegativeInt, Field
from typing import Text, List


class DocsSynthesisParams(BaseModel):
    max_goldens_per_document: NonNegativeInt = Field(default =  3, description="", )
    chunk_size: NonNegativeInt = 1024
    chunk_overlap: NonNegativeInt = 0
    num_evolutions: NonNegativeInt = 1
    enable_breadth_evolve: bool = False


class ContextSynthesisParams(BaseModel):
    max_goldens_per_context: NonNegativeInt = 3
    num_evolutions: NonNegativeInt = 1
    enable_breadth_evolve: bool = False


class ContextSynthesisSourceParams(BaseModel):
    db_name: Text = "innovation_stg_internal-trainer"
    collection_name: Text = "document_upload"
    doc_idx: NonNegativeInt = 0 


class DocsSynthesisSourceParams(BaseModel):
    document_paths: List = []
    document_folder_dir: Text = ""
