# Dagchain

This is a proof of concept repo for vectorstore loader orchestration Ⓒ.
It combines [LangChain](https://langchain.readthedocs.io/en/latest/) with [Dagster](https://docs.dagster.io/getting-started).

## ✅ Running locally
1. Install dependencies: `pip install -r requirements.txt`
2. Run `dagit -f run.py` and navigate to http://127.0.0.1:3000 to view the dags you have created. 
3. By for testing I have set up two dags in the dag folder that leverage common loading logic. To add a new loader run simply create a new file with a dagster job and add to the run.py folder.
   i. You can use any Langchain [Document Loaders](https://langchain.readthedocs.io/en/latest/modules/document_loaders.html) to load your own data into a vectorstore.

## Future
This can be used to replace the manual run of `ingest.sh` in [ChatLangChain](https://github.com/hwchase17/chat-langchain) to provide scheduled updates of vectorstores as well as handling and managing inputs from various sources.

## Next Features To Work On
