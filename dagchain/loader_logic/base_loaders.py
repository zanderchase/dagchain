from langchain.text_splitter import TextSplitter
from langchain.embeddings.base import Embeddings
from langchain.vectorstores.base import VectorStore
from langchain.document_loaders.base import BaseLoader, Document
from langchain.embeddings import OpenAIEmbeddings
import pickle
from typing import List


def load_docs_from_loaders(loader_list: List[BaseLoader]) -> List[Document]:
    docs = []
    for loader in loader_list:
        docs.extend(loader.load())
    return docs


def split_documents(
    documents: List[Document], text_splitter: TextSplitter
) -> List[Document]:
    return text_splitter.split_documents(documents)


def create_embeddings_vectorstore(
    documents: List[Document], embeddings: Embeddings, vectorstorecls: VectorStore
):
    return vectorstorecls.from_documents(documents, embeddings)


def pinecone_setup(context, documents):
    texts = [ob.page_content for ob in documents]
    embeddings = OpenAIEmbeddings()
    index_name = context.resources.pinecone
    metadatas = [ob.metadata for ob in documents]
    return [texts, embeddings, index_name, metadatas]


def save_vectorstore_to_disk(name, vectorstore):
    filename = f"{name}_vectorstore.pkl"
    with open(filename, "wb") as f:
        pickle.dump(vectorstore, f)
    return filename
