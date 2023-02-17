from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders.base import BaseLoader, Document
import pickle
from typing import List


def load_docs_from_loaders(loader_list: List[BaseLoader]) -> List[Document]:
    docs = []
    for loader in loader_list:
        docs.extend(loader.load())
    return docs


def split_documents(documents: List[Document]) -> List[Document]:
    text_splitter = RecursiveCharacterTextSplitter()
    return text_splitter.split_documents(documents)


def create_embeddings_vectorstore(documents):
    embeddings = OpenAIEmbeddings()
    return FAISS.from_documents(documents, embeddings)


def save_vectorstore_to_disk(name, vectorstore):
    filename = f"{name}_vectorstore.pkl"
    with open(filename, "wb") as f:
        pickle.dump(vectorstore, f)

    return filename
