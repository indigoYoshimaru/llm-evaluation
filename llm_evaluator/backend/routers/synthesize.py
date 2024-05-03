from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from llm_evaluator.core.app_models.params import (
    DocsSynthesisParams,
    DocsSynthesisSourceParams,
    ContextSynthesisParams,
    ContextSynthesisSourceParams,
)
from typing import Text, Any, Union
from typing_extensions import Annotated

router = APIRouter(prefix="/synthesis")


@router.post("/question-answering/context")
def create_qa_dataset_from_context(
    # db_name: Text,
    # collection_name: Text,
    data_src_params: Annotated[
        ContextSynthesisSourceParams, Depends(ContextSynthesisSourceParams)
    ],
    generator_params: Annotated[
        ContextSynthesisParams, Depends(ContextSynthesisParams)
    ],
    model: Text = "gpt-3.5-turbo-0125",
    dataset_save_dir: Text = "dataset",
):

    import os
    from llm_evaluator.core.app_models.public_configs import SynthesizerConfig
    from llm_evaluator.core.synthesizer import Synthesizer
    from llm_evaluator.templates.syn_temp import QATemplate
    from llm_evaluator.core.enums import DataSourceEnum

    try:
        data_source = DataSourceEnum.retrieve_context
        cfg_dict = data_src_params.model_dump()
        cfg_dict["generator"] = generator_params.model_dump()

        synthesizer_cfg = SynthesizerConfig(
            config_path="",
            data_source=data_source.value,
            cfg_dict=cfg_dict,
        )
        synthesizer = Synthesizer(config=synthesizer_cfg)
    except Exception as e:
        logger.error(f"{type(e).__name__}: {e} happended during loading config")
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {e}")
    try:
        document_id, dataset = synthesizer.generate(
            syn_model=model,
            template=QATemplate,
            data_source=data_source,
        )
    except Exception as e:
        logger.error(f"{type(e).__name__}: {e} happened during generating dataset")
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {e}")
    try:
        if dataset_save_dir:

            dataset_save_dir = os.path.join(
                os.getcwd(),
                dataset_save_dir,
                "qa",
            )
            if not os.path.exists(dataset_save_dir):
                os.mkdir(dataset_save_dir)
            json_data = synthesizer.save_local(dataset, dataset_save_dir, document_id)
    except Exception as e:
        logger.error(f"{type(e).__name__}: {e} Cannot save dataset")
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {e}")
    else:
        logger.success(f"Dataset generated and saved successfully")
        return json_data


# @router.post("/question-answering/docs")
# def create_qa_dataset_from_docs(): ...


# @router.post("/mqc")
# def create_mqc_dataset():
#     raise NotImplementedError(f"Working...")
