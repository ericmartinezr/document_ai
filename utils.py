import os
import base64
import logging
from consts import DOCUMENTS_DIR

logger = logging.getLogger(__name__)
logging.basicConfig(filename='app.log', encoding='utf-8', level=logging.DEBUG)


def document_to_base64(document_name: str) -> str:
    """Converst the file content to base64"""
    file_path = os.path.join(DOCUMENTS_DIR, document_name)
    if not os.path.exists(file_path):
        raise FileNotFoundError

    with open(file_path, 'rb') as file:
        content = file.read()

    return base64.b64encode(content).decode('utf-8')
