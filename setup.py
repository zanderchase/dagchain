from setuptools import setup, find_packages

setup(
    name='dagchain',
    version='1.0.0',
    url='https://github.com/mypackage.git',
    author='Zander Chase',
    author_email='zanderchase@gmail.com',
    description='Vectorstore loader orchastration package',
    packages=find_packages(),    
    install_requires=['langchain', 'openai', 'faiss-cpu', 'requests', 'beautifulsoup4', 'dagster', 'dagit'],
)
