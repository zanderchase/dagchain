from abc import ABC
from typing import List
from dagster import (
    asset,
    FreshnessPolicy,
    AssetIn,
)
from langchain.text_splitter import TextSplitter, RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.embeddings.base import Embeddings
from langchain.vectorstores.base import VectorStore
from langchain.vectorstores.faiss import FAISS
from langchain.document_loaders.base import BaseLoader
from dagchain.loader_logic.base_loaders import (
    load_docs_from_loaders,
    split_documents,
    create_embeddings_vectorstore,
    pinecone_setup,
)


class DagChainBaseLoader(ABC):
    def __init__(
        self,
        name: str,
        loader: List[BaseLoader],
        text_splitter: TextSplitter = RecursiveCharacterTextSplitter(),
        embeddings: Embeddings = OpenAIEmbeddings(),
        vectorstore_cls: VectorStore = FAISS,
        schedule: str = "@daily",
    ):
        """Initialize variables. Name, Loader, Text Splitter, Embeddings, Vectorstore Class, Schedule"""

        self.name = name
        self.loader = loader
        self.text_splitter = text_splitter
        self.embeddings = embeddings
        self.vectorstore_cls = vectorstore_cls
        self.schedule = schedule

        if not any(
            self.schedule in s for s in ["@hourly", "@daily", "@weekly", "@monthly"]
        ):
            raise ValueError(
                "Only @hourly, @daily, @weekly, @monthly schedules are supported right now"
            )

    def to_split_document_assets(self):
        @asset(
            group_name=self.name, name=f"{self.name}_raw_documents", compute_kind="http"
        )
        def raw_documents():
            "Load the raw document text from the source"
            return load_docs_from_loaders(self.loader)

        @asset(
            group_name=self.name,
            name=f"{self.name}_documents",
            ins={"raw_documents": AssetIn(f"{self.name}_raw_documents")},
            compute_kind="langchain",
        )
        def documents(raw_documents):
            "Split the documents into chunks that fit in the LLM context window"
            return split_documents(raw_documents, self.text_splitter)

        return raw_documents, documents

    def to_pinecone_assets(self):
        raw_documents, documents = self.to_split_document_assets()

        @asset(
            required_resource_keys={"pinecone"},
            io_manager_key="pinecone_io_manager",
            group_name=self.name,
            name=f"{self.name}_pinecone",
            ins={"documents": AssetIn(f"{self.name}_documents")},
            compute_kind="pinecone",
        )
        def load_pinecone(context, documents):
            "Insert the documents into pinecone vectorstore"
            return pinecone_setup(context, documents)

        return [raw_documents, documents, load_pinecone]

    def to_vectorstore_assets(self):
        raw_documents, documents = self.to_split_document_assets()

        @asset(
            group_name=self.name,
            name=f"{self.name}_vectorstore",
            io_manager_key="vectorstore_io_manager",
            freshness_policy=FreshnessPolicy(
                maximum_lag_minutes=5, cron_schedule=self.schedule
            ),
            ins={"documents": AssetIn(f"{self.name}_documents")},
            compute_kind="vectorstore",
        )
        def vectorstore(documents):
            "Compute embeddings and create a vector store"
            return create_embeddings_vectorstore(
                documents, self.embeddings, self.vectorstore_cls
            )

        return [raw_documents, documents, vectorstore]
