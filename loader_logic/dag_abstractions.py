from abc import ABC
from typing import List
from dagster import op
from dagster import (
    asset,
    Definitions,
    FreshnessPolicy,
    IOManager,
    AssetIn,
    build_asset_reconciliation_sensor,
    AssetSelection,
)
from langchain.document_loaders.base import BaseLoader
from loader_logic.base_loaders import (
    load_docs_from_loaders,
    split_documents,
    create_embeddings_vectorstore,
    save_vectorstore_to_disk,
)


class DagChainBaseLoader(ABC):
    def __init__(self, name: str, loader: List[BaseLoader], schedule="daily"):
        """Initialize with webpage path."""

        if schedule != "daily":
            raise ValueError("Only daily schedules are supported right now")

        self.name = name
        self.loader = loader
        self.schedule = schedule

    def to_assets(self):
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
            return split_documents(raw_documents)

        @asset(
            group_name=self.name,
            name=f"{self.name}_vectorstore",
            io_manager_key="vectorstore_io_manager",
            freshness_policy=FreshnessPolicy(
                maximum_lag_minutes=5, cron_schedule="0 0 * * *"
            ),
            ins={"documents": AssetIn(f"{self.name}_documents")},
            compute_kind="faiss",
        )
        def vectorstore(documents):
            "Compute embeddings and create a vector store"
            return create_embeddings_vectorstore(documents)

        return [raw_documents, documents, vectorstore]


class VectorstoreIOManager(IOManager):
    def load_input(self, context):
        raise NotImplementedError()

    def handle_output(self, context, obj):
        filename = save_vectorstore_to_disk(context.step_key, obj)
        context.add_output_metadata({"filename": filename})


def DagchainDefinitions(dagchains):
    assets = [asset for dagchain in dagchains for asset in dagchain.to_assets()]
    return Definitions(
        assets=assets,
        resources={"vectorstore_io_manager": VectorstoreIOManager()},
        sensors=[
            build_asset_reconciliation_sensor(
                AssetSelection.all(),
                name="reconciliation_sensor",
            )
        ],
    )
