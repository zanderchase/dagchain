from dagchain import (
    DagchainWeaviateDefinitions,
    DagChainBaseLoader,
)
from langchain.document_loaders import CollegeConfidentialLoader
import sys

if not sys.warnoptions:
    import warnings

    warnings.simplefilter("ignore")
##### Change your loaders as desired ######

# College loader
college_url = "https://www.collegeconfidential.com/colleges/brown-university/"
loader = CollegeConfidentialLoader(college_url)
college_dagchain = DagChainBaseLoader("college", [loader])

# Must start with an uppercase letter
client_name = "Langchain_weaviate"

# Weaviate vectorstore DB. Currently only supports 1 dagchain.
defs = DagchainWeaviateDefinitions(client_name, [college_dagchain])


def get_client_name():
    return client_name
