from langgraph.checkpoint.postgres import PostgresSaver
from langchain_core.runnables import RunnableConfig
from agents.supervisor import supervisor_agent
from utils import logger
from dotenv import load_dotenv

load_dotenv()


def run():
    user_query = """
Explain in simple words what is addernet using the document store.
"""
    config: RunnableConfig = {"configurable": {
        "thread_id": "document_extractor_1"}}

    for step in supervisor_agent.stream({
        "messages": [{"role": "user", "content": user_query}]
    }, config):
        for update in step.values():
            print(step)
            for message in update.get("messages", []):
                logger.debug(message)


if __name__ == "__main__":
    try:
        run()
    except FileNotFoundError as e:
        logger.error("File not found")
        logger.error(e, exc_info=True)
    except Exception as e:
        logger.error("Error executing main")
        logger.error(e, exc_info=True)


"""
Agente que haga lo siguiente:

- Reciba comandos por voz o texto  
(VOZ NO ME FUNCIONA EN LOCAL, TENDRIA QUE SER ALGO EN LA NUBE Y ES TODO CARISIMO Y POR MES DAN COMO 5 HORAS :) )
- Puede:
1. Leer PDFs
2. Escribir CSVs (excels)
3. Enviar email


Etnonces..

El agente va a recibir un comando como por ejemplo :

- "Extrae el contenido del PDF, guarda lo relevante en un CSV y envia un correo con el detalle"

Obviamente va a haber un agente supervisor, la lectura y extraccion de PDF es un agente,
la escritura del CSV es otro agente y el envio de correo tambien es otro agente.

El envi ode email tiene que ser po Gmail o algo, algun servicio MCP
"""


# https://github.com/Uberi/speech_recognition/blob/master/examples/microphone_recognition.py

# TODO: Testing
# https://docs.langchain.com/oss/python/langchain/test

# TODO: To attach documents
# https://docs.langchain.com/oss/python/langchain/messages#standard-content-blocks
