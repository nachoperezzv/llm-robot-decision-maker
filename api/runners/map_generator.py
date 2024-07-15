"""Map generator runner
"""

# Set PYTHONPATH of the project
import os 
import sys
import pathlib

file_path =  os.path.realpath(__file__)
root_dir = pathlib.Path(file_path).parents[1] # 2 for 2 levels etc
sys.path.insert(1, str(root_dir))

# Standard imports
import json

# Third-party imports
from openai import OpenAI
from loguru import logger

# Internal imports
from src.config import openai_config, logger_config
from src.prompts import map_generator_prompt

from src.resources import objects
from src.resources import map_level, map_configuration

client = OpenAI(api_key=openai_config.apikey)
logger.level = logger_config.level

def map_generator():
    """Generates a map
    """

    content = {
        "level": map_level, 
        "objects": objects,
        "map_configuration": map_configuration
    }
    content = map_generator_prompt.render(content)
    logger.debug(content)

    response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=1024,
        temperature=0.7,
        response_format={ "type": "json_object" }, 
        messages=[
            {"role":"system",
             "content": content}
        ]
    )

    result = response.choices[0].message.content
    result = json.loads(result)

    logger.debug(result)

    with open("map10.json", "w") as f:
        json.dump(result, f, indent=4)

if __name__ == "__main__":
    map_generator()