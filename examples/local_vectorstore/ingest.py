from dagchain import (
    DagchainDefinitions,
    DagChainBaseLoader,
)
from langchain.document_loaders import CollegeConfidentialLoader, AZLyricsLoader
import sys

if not sys.warnoptions:
    import warnings

    warnings.simplefilter("ignore")
##### Change your loaders as desired ######

# College loader
college_url = "https://www.collegeconfidential.com/colleges/brown-university/"
loader = CollegeConfidentialLoader(college_url)
college_dagchain = DagChainBaseLoader("college", [loader])

# Music loader
song_url1 = "https://www.azlyrics.com/lyrics/mileycyrus/flowers.html"
song_url2 = "https://www.azlyrics.com/lyrics/taylorswift/teardropsonmyguitar.html"
loader1 = AZLyricsLoader(song_url1)
loader2 = AZLyricsLoader(song_url2)
music_dagchain = DagChainBaseLoader("music", [loader1, loader2])

# Defs to output
# Local vectorstore
defs = DagchainDefinitions([college_dagchain])


# Pinecone vectorstore DB. Currently only supports 1 dagchain.
# defs = DagchainPineconeDefinitions(
#     "langchain_pinecone", [college_dagchain]
# )
