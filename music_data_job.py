from dagster import asset, op, job, graph, load_assets_from_package_module, OpDefinition, AssetsDefinition, AssetKey, AssetMaterialization, Definitions, ScheduleDefinition
from langchain.document_loaders import CollegeConfidentialLoader, AZLyricsLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import OpenAIEmbeddings
from loader_logic.base_loaders import source_loader, output_loader
import pickle

##### Change your loaders as desired ######
song_url1 = "https://www.azlyrics.com/lyrics/mileycyrus/flowers.html"
song_url2 = "https://www.azlyrics.com/lyrics/taylorswift/teardropsonmyguitar.html"

# Logic to set up langchain List[BaseLoader]
@asset
def college_music_loader(context):
    loader = AZLyricsLoader(song_url1)
    loader2 = AZLyricsLoader(song_url2)
    context.log_event(
        AssetMaterialization(
            asset_key="music"
        )
    )
    return [loader, loader2]


music_text = AssetsDefinition.from_op(
    source_loader.configured({"name": "music"}, name="music_text"),
    keys_by_input_name={"loader_list": AssetKey("music_loader")},
    keys_by_output_name={"result": AssetKey("music_text")},
)

music_vectorstore = AssetsDefinition.from_op(
    output_loader.configured({"name": "music"}, name="music_vectorstore"),
    keys_by_input_name={"source_loader": AssetKey("music_text")},
    keys_by_output_name={"result": AssetKey("music_vectorstore")},
)

# Logic to set up job
@job 
def load_music_vectorstore():
    music_vectorstore(music_text(college_music_loader()))