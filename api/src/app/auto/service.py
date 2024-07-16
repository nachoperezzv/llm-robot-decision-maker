"""The different services for the auto movement
"""

# Standard imports
import json
from typing import List

# Third-party imports
from openai import OpenAI
from loguru import logger

# Internal imports
from src.app.auto.schemas.input import Point, Object

from src.config import openai_config, logger_config
from src.resources.objects import objects
from src.prompts import auto_service_prompt


client = OpenAI(api_key=openai_config.apikey)
logger.level = logger_config.level


def decide_action(robot: Point, env_objects: List[Object], close_objects: List[Object]) -> str:
    """Makes a request to Openai API

    Arguments:
        robot (Point): Where robot is
        env_objects (List[Object]): List of position of all the objects in the map.
        close_objects (List[Object]): List of position of the close objects in the map. 

    Returns:
        (str)
    """

    content = {
        "robot": robot, 
        "objects": objects,
        "env_objects": env_objects, 
        "close_objects": close_objects
    }
    content = auto_service_prompt.render(content)
    
    logger.debug(content)

    response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=1024,
        temperature=0.0,
        response_format={ "type": "json_object" }, 
        messages=[
            {"role":"system",
             "content": content}
        ]
    )
    
    result = response.choices[0].message.content
    result = json.loads(result)

    logger.debug(result)

    return result
