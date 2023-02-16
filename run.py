from loader_logic.dag_abstractions import DagChainBaseLoader, SetDefinitions
from langchain.document_loaders import CollegeConfidentialLoader, AZLyricsLoader

##### Change your loaders as desired ######

# College loader
college_url = "https://www.collegeconfidential.com/colleges/university-of-chicago/"
loader = CollegeConfidentialLoader(college_url)
college_dagchain = DagChainBaseLoader("college", [loader], 'daily')
college_job, college_schedule = college_dagchain.setup_job()

# Music loader
song_url1 = "https://www.azlyrics.com/lyrics/mileycyrus/flowers.html"
song_url2 = "https://www.azlyrics.com/lyrics/taylorswift/teardropsonmyguitar.html"
loader1 = AZLyricsLoader(song_url1)
loader2 = AZLyricsLoader(song_url2)


music_dagchain = DagChainBaseLoader("music", [loader1, loader2], 'daily')
music_job, music_schedule = music_dagchain.setup_job()

# Defs to output
defs = SetDefinitions(
    jobs=[music_job, college_job],
    schedules=[music_schedule, college_schedule],
)