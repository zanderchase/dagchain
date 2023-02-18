from loader_logic.dag_abstractions import DagChainBaseLoader, DagchainDefinitions
from langchain.document_loaders import CollegeConfidentialLoader, AZLyricsLoader

##### Change your loaders as desired ######

# College loader
college_url = "https://www.collegeconfidential.com/colleges/university-of-chicago/"
loader = CollegeConfidentialLoader(college_url)
college_dagchain = DagChainBaseLoader("college", [loader])

# Music loader
song_url1 = "https://www.azlyrics.com/lyrics/mileycyrus/flowers.html"
song_url2 = "https://www.azlyrics.com/lyrics/taylorswift/teardropsonmyguitar.html"
loader1 = AZLyricsLoader(song_url1)
loader2 = AZLyricsLoader(song_url2)
music_dagchain = DagChainBaseLoader("music", [loader1, loader2])

# Defs to output
defs = DagchainDefinitions([college_dagchain, music_dagchain])
