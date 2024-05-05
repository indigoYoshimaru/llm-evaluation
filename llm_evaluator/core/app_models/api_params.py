from pydantic import BaseModel, NonNegativeInt, Field
from typing import Text, List, Dict


class DocsSynthesisParams(BaseModel):
    max_goldens_per_document: NonNegativeInt = Field(
        default=3,
        description="",
    )
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


class GenEvaluatorMetricParams(BaseModel):
    metrics: Dict = dict(
        faithfulness=True,
        hallucination=False,
        answer_relevancy=False,
        bias=False,
        toxicity=False,
    )

    metric_params: Dict = dict(
        threshold=0.5,
        include_reason=True,
        async_mode=True,
    )


class RetEvaluatorMetricParams(BaseModel):
    metrics: Dict = dict(
        context_rouge=True,
        context_bleu=False,
        contextual_precision=False,
        contextual_recall=False,
        contextual_relevancy=False,
    )

    metric_params: Dict = dict(
        threshold=0.5,
        include_reason=True,
        async_mode=True,
    )


class EvaluatorSourceParams(BaseModel):
    db_name: Text = "innovation_stg_internal-trainer"
    collection_name: Text = "chat_ticket"
    model_url: Text = (
        "https://api.stg.buymed.tech/buymed-innovation/internal-trainer/v1/chat"
    )
