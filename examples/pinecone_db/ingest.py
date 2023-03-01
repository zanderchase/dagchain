from dagchain import (
    DagchainPineconeDefinitions,
    DagChainBaseLoader,
)
from langchain.document_loaders import CollegeConfidentialLoader

##### Change your loaders as desired ######

# College loader
college_url = "https://www.collegeconfidential.com/colleges/university-of-chicago/"
loader = CollegeConfidentialLoader(college_url)
college_dagchain = DagChainBaseLoader("college", [loader])

# Pinecone vectorstore DB. Currently only supports 1 dagchain.
defs = DagchainPineconeDefinitions("langchain_pinecone", [college_dagchain])
