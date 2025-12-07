from agents.supervisor import supervisor_agent
from utils import document_to_base64, logger
from dotenv import load_dotenv

load_dotenv()


def run():
    user_query = """
Extract the following information from the attached PDF:

- Name
- Phone number
- Address

**Instructions**
- If there is no PDF attached return the following message: "I can't extract information, there's no PDF attached"

"""
    # TODO: Esto no está funcionando
    # asi que es mejor convertirlo a vector y guardarlo en PGVector
    doc_base64 = document_to_base64(
        "Small Language Models are the Future of Agentic AI.pdf")

    logger.debug("Document base64")
    logger.debug(doc_base64)

    for step in supervisor_agent.stream({
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text", "text": user_query
                    },
                    {
                        "type": "file",
                        "base64": doc_base64,
                        "mime_type": "application/pdf",
                    }
                ]

            },
        ]
    }):
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
