import base64
import json
from loguru import logger
from typing import Dict, List


def decode(data_dict: Dict):
    for k, v in data_dict.items():
        try:
            data_dict[k] = json.loads(
                base64.b64decode(v, validate=False).decode("utf-8")
            )
        except Exception as e:
            logger.warning(
                f"{type(e).__name__}: {e}. May not be encoded string, reuse the original value"
            )
            data_dict[k] = v
    return data_dict


def encode(data_dict: Dict, ignored: List = []):
    for k, v in data_dict.items():
        if k in ignored:
            continue
        data_dict[k] = base64.b64encode(json.dumps(v).encode("utf-8")).decode()
        print(type(data_dict[k]))
    return data_dict
