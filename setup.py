from setuptools import setup, find_packages

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setup(
    name="dagchain",
    version="0.0.1",
    url="https://github.com/zanderchase/dagchain",
    author="Zander Chase",
    author_email="zanderchase@gmail.com",
    description="Python package for vectorstore loader orchastration",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    packages=find_packages(where="dagchain"),
    install_requires = [
        "langchain",
        "dagster",
        "openai",
        "faiss-cpu",
        "pinecone-client",
    ],
    python_requires = ">=3.6"
)
