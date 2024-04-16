from llm_evaluator.utils import fileio
import json
import base64


reader = fileio.FileReader()

cfg = reader.read(".vscode/launch.json")
db_cfg = cfg["env"]["database"]
decoded_bytes = base64.b64decode(db_cfg, validate=False)
decoded_string = decoded_bytes.decode("utf-8")
config_map = json.loads(decoded_string)
print(config_map)
env_cfg = cfg["env"]["service"]
decoded_bytes = base64.b64decode(env_cfg, validate=False)
decoded_string = decoded_bytes.decode("utf-8")
env_cfg = json.loads(decoded_string)
print(env_cfg)


from pymongo.mongo_client import MongoClient

connection_str = "mongodb://{user}:{password}@{address}/?authSource={auth}".format(
    **config_map["db"]
).replace("?replicaSet=rs/", "").replace("@mongodb://", "@")
print(connection_str)
db = MongoClient(connection_str)
col = db['innovation_stg_internal-trainer']['document_upload']

# from markdownify import markdownify as md

# for doc in col.find(): 
#     print(md(doc['content']))
