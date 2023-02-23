from dagster import (
    IOManager,
    Definitions,
    build_asset_reconciliation_sensor,
    AssetSelection,
)
from dagchain.loader_logic.base_loaders import save_vectorstore_to_disk


class VectorstoreIOManager(IOManager):
    def load_input(self, context):
        raise NotImplementedError()

    def handle_output(self, context, obj):
        filename = save_vectorstore_to_disk(context.step_key, obj)
        context.add_output_metadata({"filename": filename})


def DagchainDefinitions(dagchains):
    assets = [
        asset for dagchain in dagchains for asset in dagchain.to_vectorstore_assets()
    ]
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
