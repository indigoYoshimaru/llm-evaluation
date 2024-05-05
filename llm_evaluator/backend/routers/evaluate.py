from fastapi import APIRouter, Depends, UploadFile, HTTPException
from loguru import logger
from typing import Annotated
from llm_evaluator.core.app_models.api_params import (
    EvaluatorSourceParams,
    GenEvaluatorMetricParams,
    RetEvaluatorMetricParams,
)

from llm_evaluator.core.app_models.public_configs import EvaluatorConfig
from typing import Text
from llm_evaluator.core.evaluator import Evaluator

router = APIRouter(prefix="/evaluate")


@router.post("/upload-dataset")
def upload_dataset(dataset: UploadFile):
    if not dataset.filename.endswith(".json"):
        raise HTTPException(status_code=415, detail="Expected JSON file")
    try:
        file_location = f"dataset/upload/{dataset.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(dataset.file.read())
    except Exception as e:
        logger.error(f"{type(e).__name__}: {e}")
        raise HTTPException(status_code=409, detail=f"{type(e).__name__}: {e}")
    else:
        msg = f"Uploaded file {dataset.filename}"
        logger.info(msg)
        return msg


@router.post("/generator")
def eval_generator(
    src_params: Annotated[EvaluatorSourceParams, Depends(EvaluatorSourceParams)],
    metrics_option: Annotated[
        GenEvaluatorMetricParams, Depends(GenEvaluatorMetricParams)
    ],
    dataset_filename: Text,
    judge_model: Text = "gpt-3.5-turbo-0125",
):
    from llm_evaluator.core.enums import QuestionTypeEnum

    try:
        # NEEDS UPDATING TO DB SAVE
        import os

        dataset_path = str(
            os.path.join(
                os.getcwd(),
                "dataset/upload",
                dataset_filename,
            )
        )
        assert os.path.isfile(dataset_path), "Dataset not found"
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)
    try:
        cfg_dict = src_params.model_dump()
        cfg_dict.update(metrics_option.model_dump())
        eval_cfg = EvaluatorConfig(config_path="", cfg_dict=cfg_dict)
        evaluator = Evaluator(
            config=eval_cfg,
            question_type=QuestionTypeEnum.qa.name,
            judge_model=judge_model,
        )
        test_results = evaluator.evaluate(dataset_path=dataset_path)

    except Exception as e:
        logger.error(f"{type(e).__name__}: {e}")
        raise HTTPException(
            status_code=500, detail=f"{type(e).__name__}: {e} Cannot run evaluation"
        )
    else:
        logger.success(f"Evaluated dataset {dataset_path}")
        # os.remove(dataset_path)
        return test_results


@router.post("/retriever")
def eval_retriever(
    src_params: Annotated[EvaluatorSourceParams, Depends(EvaluatorSourceParams)],
    metrics_option: Annotated[
        RetEvaluatorMetricParams, Depends(RetEvaluatorMetricParams)
    ],
    dataset_filename: Text,
    judge_model: Text = "gpt-3.5-turbo-0125",
):
    from llm_evaluator.core.enums import QuestionTypeEnum

    try:
        # NEEDS UPDATING TO DB SAVE
        import os

        dataset_path = str(
            os.path.join(
                os.getcwd(),
                "dataset/upload",
                dataset_filename,
            )
        )
        assert os.path.isfile(dataset_path), "Dataset not found"
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)
    try:
        cfg_dict = src_params.model_dump()
        cfg_dict.update(metrics_option.model_dump())
        eval_cfg = EvaluatorConfig(config_path="", cfg_dict=cfg_dict)
        evaluator = Evaluator(
            config=eval_cfg,
            question_type="rag",
            judge_model=judge_model,
        )
        test_results = evaluator.evaluate(dataset_path=dataset_path)

    except Exception as e:
        logger.error(f"{type(e).__name__}: {e}")
        raise HTTPException(
            status_code=500, detail=f"{type(e).__name__}: {e} Cannot run evaluation"
        )
    else:
        logger.success(f"Evaluated dataset {dataset_path}")
        # os.remove(dataset_path)
        return test_results
    
    
