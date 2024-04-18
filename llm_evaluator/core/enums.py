from enum import Enum

class DataSourceEnum(str, Enum):
    retrieve_context = "context"
    retrieve_document_paths = "document_paths"
    retrieve_document_paths_from_folder_dir = "folder_dir"


class QuestionTypeEnum(str, Enum): 
    mqc = "multiple-choice"
    qa = "question-answer"