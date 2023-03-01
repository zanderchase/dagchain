from langchain import OpenAI, VectorDBQA
from langchain.agents import Tool
from langchain.vectorstores.weaviate import Weaviate
from examples.weaviate_db.ingest import get_client_name
from dagchain import WeaviateClient

llm = OpenAI(temperature=0)


def get_vector():
    # Update on change
    client = WeaviateClient()
    index_name = get_client_name()
    weaviate_vectorstore = Weaviate(client, index_name, "content")
    return VectorDBQA.from_chain_type(
        llm=llm, chain_type="stuff", vectorstore=weaviate_vectorstore
    )


def get_tool():
    # Update on change
    return Tool(
        name="Weaviate College QA System",
        func=get_vector().run,
        description="""Useful for when you need to answer questions about colleges. 
        Input should be a fully formed question.""",
    )
