FAISS_INDEX = "files/faiss_index"
EMBEDDINGS_MODEL = "text-embedding-3-large"
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model=EMBEDDINGS_MODEL)
vector_db = FAISS.load_local(
    FAISS_INDEX,
    embeddings,
    allow_dangerous_deserialization=True,
)
print(vector_db)
print(type(vector_db.index))
print(vector_db.docstore)
# cannot indicing the database! 