# Dagchain

## Quick Install

`pip install dagchain`

## 🤔 What is this?

This is a proof of concept repo for vectorstore loader orchestration Ⓒ.
It combines [LangChain](https://langchain.readthedocs.io/en/latest/) with [Dagster](https://docs.dagster.io/getting-started).

## ✅ Run an example

We have created an example to show how to get started with this.

1. Clone this repo
2. Go into repository for examples `cd examples`
3. Install dependencies: `pip install -r requirements.txt`
4. Set OPENAI_API_KEY environment variable `export OPENAI_API_KEY={YOUR_API_KEY}`
5. Run `dagster dev -f main.py` and navigate to http://127.0.0.1:3000/ to view the dag jobs you have created.
6. run.py's default is to store the output to a local vectorstore .pkl file. See alternative storage options below.

For testing I have set up two dags in the dag folder that leverage common loading logic. To add a new loader run simply create a new file with a dagster job and add to the run.py folder.
   i. You can use any Langchain [Document Loaders](https://langchain.readthedocs.io/en/latest/modules/document_loaders.html) to load your own data into a vectorstore.


## Storage

### Pinecone
To run with Pinecone Vector Database you will need to:
1. Sign up for an account here: [Pinecone](https://www.pinecone.io/)
2. Navigate to API Key page and set two environment variables `export PINECONE_API_KEY={YOUR_API_KEY}` and `export PINECONE_ENVIRONMENT={YOUR_ENVIRONMENT}`
3. Uncomment the Pinecone def in the run.py file and comment the previous def.
4. Run `dagster dev -f run.py` and navigate to http://127.0.0.1:3000/ to view the dag jobs you have created.


## Future

This can be used to replace the manual run of `ingest.sh` in [ChatLangChain](https://github.com/hwchase17/chat-langchain) to provide scheduled updates of vectorstores as well as handling and managing inputs from various sources.

## Sample View

<img width="675" alt="Screen Shot 2023-02-17 at 2 35 52 PM" src="https://user-images.githubusercontent.com/22759784/219800978-ee2ad358-82ad-4107-9afc-4cc86831a063.png">

## Contributing Guide

To build package:

0. Clean up any artifacts from before: `rm -rf dist`
1. Build package: `python -m build` (will create `dist` folder)
2. Upload package: `twine upload dist/*`
