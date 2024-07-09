"""Ouput schemas for /auto endpoint
"""

# Standard imports
from typing import Union
from typing import List

# Third-party imports
from pydantic import BaseModel

class Point(BaseModel):
    x: int
    y: int

class Object(BaseModel):
    id: str
    pos: Point

class EnvResponse(BaseModel):
    robot: Point
    objects: Union[List[Object], None]
    thoughts: List[str]