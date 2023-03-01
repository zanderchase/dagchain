from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="dagchain",
    version="0.0.1",
    url="https://github.com/zanderchase/dagchain",
    author="Zander Chase",
    author_email="zanderchase@gmail.com",
    description="Vectorstore loader orchastration package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "langchain",
        "dagster",
        "dagit",
    ],
)
