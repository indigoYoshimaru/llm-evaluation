from fastapi import APIRouter, UploadFile, HTTPException
from loguru import logger
from typing import Text


router = APIRouter(prefix="dataset")


@router.post("/upload")
def upload_dataset(dataset: UploadFile):
    if not dataset.filename.endswith(".json"):
        raise HTTPException(status_code=415, detail="Expected JSON file")
    try:
        import os

        file_location = f"dataset/{dataset.filename}"
        assert os.path.isfile(
            file_location
        ), f"Dataset with name {dataset.filename} already exists"
        with open(file_location, "wb+") as file_object:
            file_object.write(dataset.file.read())
    except AssertionError as e:
        logger.error(f"{type(e).__name__}: {e}")
        raise HTTPException(status_code=400, detail=f"{e}")
    except Exception as e:
        logger.error(f"{type(e).__name__}: {e}")
        raise HTTPException(status_code=409, detail=f"{type(e).__name__}: {e}")
    else:
        msg = f"Uploaded file {dataset.filename}"
        logger.info(msg)
        return msg


@router.post("/delete")
def delete_dataset(dataset_name: Text):
    import os

    file_ext = ".json"  # hardcode since we only use json for now!
    try:
        if not dataset_name.endswith(file_ext):
            dataset_name += file_ext
        dataset_path = f"dataset/{dataset_name}"
        assert os.path.isfile(dataset_path), f"Dataset {dataset_name} not found!"
        os.remove(dataset_path)
    except AssertionError as e:
        logger.error(f"{type(e).__name__}: {e}")
        raise HTTPException(status_code=400, detail=f"{e}")
    except Exception as e:
        msg = f"Cannot delete {dataset_name} due to error {type(e).__name__}: {e}"
        logger.error(msg)
        raise HTTPException(status_code=405, detail=msg)
    else:
        msg = f"Deleted file {dataset_name}"
        logger.info(msg)
        return msg
