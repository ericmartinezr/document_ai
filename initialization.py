# Initializes the vectore store with the documents found in the folder

import os
from langchain_docling.loader import DoclingLoader, ExportType
from stores import document_store
from consts import DOCUMENTS_DIR

if not os.path.exists(DOCUMENTS_DIR):
    raise ValueError(f"Directory {DOCUMENTS_DIR} doesn't exist")

allowed_exts = ['pdf', 'doc', 'docx']
files_to_ingest = [
    os.path.join(DOCUMENTS_DIR, file)
    for file in os.listdir(DOCUMENTS_DIR)
    if file.split('.')[-1] in allowed_exts]


loader = DoclingLoader(
    file_path=files_to_ingest,
    export_type=ExportType.DOC_CHUNKS)

docs = loader.load_and_split()

document_store.add_documents(documents=docs)
