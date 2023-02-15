from dagster import asset, op, job, graph, load_assets_from_package_module, OpDefinition, AssetsDefinition, AssetKey, AssetMaterialization, Definitions, ScheduleDefinition
from langchain.document_loaders import CollegeConfidentialLoader, AZLyricsLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import OpenAIEmbeddings
from loader_logic.base_loaders import source_loader, output_loader
from dags.music_data_job import load_music_vectorstore
from dags.college_data_job import load_college_vectorstore

import pickle






# Logic to load source loader



# Logic to save text docs in vectorstore


# Schedule setup
basic_music_schedule = ScheduleDefinition(job=load_music_vectorstore, cron_schedule="0 0 * * *")
basic_college_schedule = ScheduleDefinition(job=load_college_vectorstore, cron_schedule="0 0 * * *")

# Defs to output
defs = Definitions(
    jobs=[load_music_vectorstore, load_college_vectorstore],
    schedules=[basic_music_schedule, basic_college_schedule],
)
