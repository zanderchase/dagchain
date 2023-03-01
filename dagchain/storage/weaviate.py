from dagster import (
    IOManager,
    Definitions,
    build_asset_reconciliation_sensor,
    AssetSelection,
    resource,
)

from langchain.vectorstores.weaviate import Weaviate
import os


class WeaviateIOManager(IOManager):
    def load_input(self, context):
        raise NotImplementedError()

    def handle_output(self, context, obj):
        client = WeaviateClient()
        client.schema.delete_all()
        index_name = obj[1]
        class_obj = {
            "class": index_name,
            "vectorizer": "text2vec-openai",
        }
        client.schema.create_class(class_obj)
        vectorstore = Weaviate(client, index_name, "content")
        vectorstore.add_texts(
            texts=obj[0],
            metadatas=obj[2],
        )
        context.add_output_metadata({"weaviate_index": obj[2]})


def DagchainWeaviateDefinitions(name, dagchains):
    assets = [
        asset for dagchain in dagchains for asset in dagchain.to_weaviate_assets()
    ]
    index_name = name.replace("_", "-")
    # WeaviateClient()

    @resource
    def weaviate_index_name():
        return index_name

    return Definitions(
        assets=assets,
        resources={
            "weaviate": weaviate_index_name,
            "weaviate_io_manager": WeaviateIOManager(),
        },
        sensors=[
            build_asset_reconciliation_sensor(
                AssetSelection.all(),
                name="reconciliation_sensor",
            )
        ],
    )


# def DagchainPineconeOutput(index, query):
#     embedding = OpenAIEmbeddings()
#     embed = embedding.embed_documents(query)
#     xq = embed["data"][0]["embedding"]
#     res = index.query(xq, top_k=2, include_metadata=True)
#     return res


def WeaviateClient():
    if os.environ.get("WEAVIATE_URL") is None:
        raise ValueError("WEAVIATE_URL is not set")
    import weaviate

    client = weaviate.Client(
        url=os.getenv("WEAVIATE_URL"),
        additional_headers={"X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")},
    )
    return client
