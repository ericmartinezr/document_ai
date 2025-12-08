# Initializes the vectore store with the documents found in the folder

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from stores import document_store
from consts import DOCUMENTS_DIR
from utils import logger

if not os.path.exists(DOCUMENTS_DIR):
    raise ValueError(f"Directory {DOCUMENTS_DIR} doesn't exist")

allowed_exts = ['pdf', 'doc', 'docx']
files_to_ingest = [
    os.path.join(DOCUMENTS_DIR, file)
    for file in os.listdir(DOCUMENTS_DIR)
    if file.split('.')[-1] in allowed_exts]

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=200,
    add_start_index=True,
    separators=["\n\n", "\n"]
)

for file in files_to_ingest:
    logger.info(f"Splitting document {file}")

    loader = PyPDFLoader(
        file_path=file,
        mode="page",
        extract_images=False,
        extraction_mode="plain")

    docs = loader.load_and_split(text_splitter)

    logger.info(f"There's a total of {len(docs)} documents")

    document_store.add_documents(documents=docs)

    logger.info(f"Document {file} splitted succesfully")


# TODO: Revisar este error
"""

sqlalchemy.exc.DataError: (psycopg.DataError) PostgreSQL text fields cannot contain NUL (0x00) bytes
[SQL: INSERT INTO "public"."documents"("langchain_id", "content", "embedding", "langchain_metadata")VALUES (%(langchain_id)s, %(content)s, %(embedding)s, %(extra)s) ON CONFLICT ("langchain_id") DO UPDATE SET "content" = EXCLUDED."content", "embedding" = EXCLUDED."embedding", "langchain_metadata" = EXCLUDED."langchain_metadata";]
[parameters: {'langchain_id': '50e5e4f4-d8d0-4f47-bf4d-9d73200fa5f9', 'content': 'mechanismretrieves only the key-value entries {c𝑠}corresponding to the top-k index scores.\nThen, the attention outputu 𝑡 is computed by   applying the ... (27 characters truncated) ... n the\nquery tokenh 𝑡 and the sparsely selected key-value entries{c 𝑠}  :\nu𝑡 =Attn \x00h𝑡
,\n\x08\nc𝑠\n\x0c\x0c 𝐼𝑡,𝑠 ∈Top-k \x00\n𝐼𝑡,:\n\x01\t\x01. (2)', 'embedding': '[0.041410223, -0      .022345139, 0.022022814, -0.02766551, 0.0116234515, -0.00080101704, -0.0051883413, -0.034831524, 0.024899106, 0.0024031135, -0.028250 ... (55850 characters truncated) ... .01958543, 0.0027297295, 0.009847139, -0.0077052484, -0.019111067, 0.00017132932, -0.008680239, 0.006089941, -0.024730597, 0.001145898, -0.020047886]', 'extra': '{"producer": "pdfTeX-1.40.27", "creator": "LaTeX with hyperref", "creationdate": "2025-09-29T08:49:11+00:00", "author": "", "keywords": "", "moddate" ... (176 characters truncated) ... ": "/False", "source": "/home/eric/voice_commander/documents/DeepSeek_V3_2.pdf", "total_pages": 6, "page": 0, "page_label": "1", "start_index": 1672}'}]
(Background on this error at: https://sqlalche.me/e/20/9h9h)
"""
