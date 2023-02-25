from setuptools import setup, find_packages

setup(
    name="dagchain",
    version="0.0.1",
    url="https://github.com/zanderchase/dagchain",
    author="Zander Chase",
    author_email="zanderchase@gmail.com",
    description="Vectorstore loader orchastration package",
    packages=find_packages(),
    install_requires=[
        "langchain",
        "dagster",
        "dagit",
    ],
)
