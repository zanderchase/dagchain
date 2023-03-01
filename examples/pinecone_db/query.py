from langchain.embeddings.openai import OpenAIEmbeddings
from langchain import OpenAI, VectorDBQA
from langchain.agents import Tool
from langchain.vectorstores.pinecone import Pinecone
from dagchain import PineconeIndex

llm = OpenAI(temperature=0)


def GetVector():
    # Update on change
    index = PineconeIndex("langchain_pinecone")
    embeddings = OpenAIEmbeddings()
    pinecone_vectorstore = Pinecone(index, embeddings.embed_query, "text")
    return VectorDBQA.from_chain_type(
        llm=llm, chain_type="stuff", vectorstore=pinecone_vectorstore
    )


def GetTool():
    # Update on change
    return Tool(
        name="Pinecone College QA System",
        func=GetVector().run,
        description="""Useful for when you need to answer questions about colleges. 
        Input should be a fully formed question.""",
    )
