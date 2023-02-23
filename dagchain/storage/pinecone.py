from dagster import (
    IOManager,
    Definitions,
    build_asset_reconciliation_sensor,
    AssetSelection,
    resource,
)
import pinecone
import numpy as np
from langchain.vectorstores.pinecone import Pinecone
from langchain.embeddings import OpenAIEmbeddings
import os


class PineconeIOManager(IOManager):
    def load_input(self, context):
        raise NotImplementedError()

    def handle_output(self, context, obj):
        index_name = obj[2]
        if index_name in pinecone.list_indexes():
            pinecone.delete_index(index_name)
        Pinecone.from_texts(
            obj[0],
            obj[1],
            index_name=index_name,
            metadatas=obj[3],
            namespace="dagchain-documents",
        )
        context.add_output_metadata({"pineconde_index": obj[2]})


def DagchainPineconeDefinitions(name, dagchains):
    assets = [
        asset for dagchain in dagchains for asset in dagchain.to_pinecone_assets()
    ]

    @resource
    def pinecone_index_name():
        index_name = name.replace("_", "-")
        return index_name

    return Definitions(
        assets=assets,
        resources={
            "pinecone": pinecone_index_name,
            "pinecone_io_manager": PineconeIOManager(),
        },
        sensors=[
            build_asset_reconciliation_sensor(
                AssetSelection.all(),
                name="reconciliation_sensor",
            )
        ],
    )


def DagchainPineconeOutput(index, query):
    embedding = OpenAIEmbeddings()
    embed = embedding.embed_documents(query)
    xq = embed["data"][0]["embedding"]
    res = index.query(xq, top_k=2, include_metadata=True)
    return res


def PineconeIndex(name):
    api_key = os.getenv("PINECONE_API_KEY")
    environment = os.getenv("PINECONE_ENVIRONMENT")
    pinecone.init(api_key=api_key, environment=environment)
    index_name = name.replace("_", "-")
    index = pinecone.Index(index_name=index_name)
    return index
