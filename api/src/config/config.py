"""Config file
"""

# Standard imports
from os import getenv
from dataclasses import dataclass

# Third-party imports
from dotenv import load_dotenv

load_dotenv()

@dataclass(repr=False)
class OpenAIConfig:
    apikey:str = getenv("OPENAI_API_KEY")

@dataclass(repr=False)
class LoggerConfig:
    level:str = "DEBUG"

openai_config = OpenAIConfig()
logger_config = LoggerConfig()