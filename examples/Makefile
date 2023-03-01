ingest-local:
	dagster dev -f local_vectorstore/ingest.py

ingest-pinecone:
	dagster dev -f pinecone_db/ingest.py

ingest-weaviate:
	dagster dev -f weaviate_db/ingest.py
	
run-local:
	python3 main.py local_vectorstore

run-pinecone:
	python3 main.py pinecone_db

run-weaviate:
	python3 main.py weaviate_db
