from abc import ABC
from typing import List
from dagster import op
from dagster import asset, op, job, AssetsDefinition, AssetKey, ScheduleDefinition, Definitions
from langchain.document_loaders.base import BaseLoader
from loader_logic.base_loaders import source_loader, output_loader

class DagChainBaseLoader(ABC):

    def __init__(self, name: str, loader: List[BaseLoader], schedule='daily'):
        """Initialize with webpage path."""
        self.name = name
        self.loader = loader
        self.schedule = schedule

    def setup_job(self):

        @asset(name=f"{self.name}_load")
        def load():
            asset_loader = self.loader
            return asset_loader

        embedding = AssetsDefinition.from_op(
            source_loader.configured({"name": f"{self.name}"}, name=f"{self.name}_text"),
            keys_by_input_name={"loader_list": AssetKey(f"{self.name}_loader")},
            keys_by_output_name={"result": AssetKey(f"{self.name}_text")},
        )

        vectorstore = AssetsDefinition.from_op(
            output_loader.configured({"name": f"{self.name}"}, name=f"{self.name}_vectorstore"),
            keys_by_input_name={"source_loader": AssetKey(f"{self.name}_text")},
            keys_by_output_name={"result": AssetKey(f"{self.name}_vectorstore")},
        )


        @job(name=f"{self.name}_job")
        def load_vectorstore():
            vectorstore(embedding(load()))

        
        if self.schedule != 'daily':
            print('Warning: only daily schedule supported right now')

        schedule = ScheduleDefinition(job=load_vectorstore, name=f"{self.name}_schedule", cron_schedule="0 0 * * *")

        return load_vectorstore, schedule

def SetDefinitions(jobs, schedules):
    defs = Definitions(
        jobs=jobs,
        schedules=schedules,
    )
    return defs
