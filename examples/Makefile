local-ingest:
	dagster dev -f local_vectorstore/ingest.py
	
local-run:
	python3 main.py local_vectorstore

pinecone-ingest:
	dagster dev -f pinecone_db/ingest.py

pinecone-run:
	python3 main.py pinecone_db