from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import OpenAIEmbeddings
from dagster import op
import pickle

@op(config_schema={"name": str})
def source_loader(loader_list):
    loaders = loader_list
    docs = []
    for loader in loaders:
        docs.extend(loader.load())   
    return list(docs)


@op(config_schema={"name": str})
def output_loader(context, source_loader):
    name = context.op_config["name"]
    filename = f"{name}_vectorstore.pkl"
    # Split text
    text_splitter = RecursiveCharacterTextSplitter()
    documents = text_splitter.split_documents(source_loader)

    # Load Data to vectorstore
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)

    # Save vectorstore
    with open(filename, "wb") as f:
        pickle.dump(vectorstore, f)

    return filename