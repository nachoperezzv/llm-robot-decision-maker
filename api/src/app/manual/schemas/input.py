"""Input schemas for /manual endpoint
"""

# Standard imports
from typing import Union, Literal
from typing import List

# Third-party imports
from pydantic import BaseModel

class Point(BaseModel):
    x: int
    y: int

class Object(BaseModel):
    id: str
    pos: Point
    
class ManualEnvRequest(BaseModel):
    mov: Union[Literal["N", "E", "S", "O"], None]
    action: Union[Literal["D", "M", "R"], None]
    robot: Point
    env_objects: Union[List[Object], None]