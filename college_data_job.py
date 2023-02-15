from dagster import asset, op, job, graph, load_assets_from_package_module, OpDefinition, AssetsDefinition, AssetKey, AssetMaterialization, Definitions, ScheduleDefinition
from langchain.document_loaders import CollegeConfidentialLoader, AZLyricsLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import OpenAIEmbeddings
from loader_logic.base_loaders import source_loader, output_loader
import pickle

##### Change your loaders as desired ######
college_url = "https://www.collegeconfidential.com/colleges/university-of-chicago/"


@asset
def college_loader(context):
    loader = CollegeConfidentialLoader(college_url)
    context.log_event(
        AssetMaterialization(
            asset_key="college"
        )
    )
    return [loader]

college_text = AssetsDefinition.from_op(
    source_loader.configured({"name": "college"}, name="college_text"),
    keys_by_input_name={"loader_list": AssetKey("college_loader")},
    keys_by_output_name={"result": AssetKey("college_text")},
)

college_vectorstore = AssetsDefinition.from_op(
    output_loader.configured({"name": "college"}, name="college_vectorstore"),
    keys_by_input_name={"source_loader": AssetKey("college_text")},
    keys_by_output_name={"result": AssetKey("college_vectorstore")},
)

# Logic to set up job
@job 
def load_college_vectorstore():
    college_vectorstore(college_text(college_loader()))