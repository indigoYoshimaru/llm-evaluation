from typing import Text, List
from loguru import logger
import os
from llm_evaluator.utils.fileio import FileWriter


def save_dataset(
    dataset: List,
    dataset_save_dir: Text,
    document_id: Text,
):
    try:
        if not os.path.exists(dataset_save_dir):
            os.mkdir(dataset_save_dir)

        dataset_path = os.path.join(dataset_save_dir, f"{document_id}.json")
        FileWriter().write(file_path=dataset_path, content=dataset)

    except Exception as e:
        raise e
    else:
        logger.success(f"Saved dataset to {dataset_save_dir}")
