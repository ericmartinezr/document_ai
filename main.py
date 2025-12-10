from langchain_core.runnables import RunnableConfig
from langchain_redis import RedisCache
from langchain_core.globals import set_llm_cache
from agents.supervisor import supervisor_agent
from utils import logger
from dotenv import load_dotenv

load_dotenv()

# TODO: See if I need to add TTL to cache entries
redis_cache = RedisCache(redis_url="redis://localhost:6379")
set_llm_cache(redis_cache)


def run():
    user_query = """
Extract the dense features results from DINOv3. Get the author and the publish date from the papater. 
After you have extracted the information, write them to a csv file and send an email with the detail.
"""
    config: RunnableConfig = {"configurable": {
        "thread_id": "document_extractor_1"}}

    for step in supervisor_agent.stream({
        "messages": [{"role": "user", "content": user_query}]
    }, config):
        for update in step.values():
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
