from langchain import OpenAI, VectorDBQA
from langchain.agents import Tool
import pickle

llm = OpenAI(temperature=0)

# Update on change
vectorstore_file = "college_vectorstore_vectorstore.pkl"

with open(vectorstore_file, "rb") as f:
    global vectorstore
    local_vectorstore = pickle.load(f)


def get_vector():
    return VectorDBQA.from_chain_type(
        llm=llm, chain_type="stuff", vectorstore=local_vectorstore
    )


def get_tool():
    # Update on change
    return Tool(
        name="Local Vectorstore College QA System",
        func=get_vector().run,
        description="""Useful for when you need to answer questions about colleges. 
        Input should be a fully formed question.""",
    )
