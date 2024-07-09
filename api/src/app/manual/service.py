"""The different services for the manual movement
"""

# Standard imports
from typing import List

# Third-party imports
from fastapi import HTTPException  

# Internal imports
from src.app.manual.schemas.input import Point, Object
from src.app.objects import walls, blocks, stickman, price
from src.app.constants import WIDTH, HEIGHT

MOVS = {
    "N": Point(x=0, y=-1), 
    "E": Point(x=1, y=0), 
    "S": Point(x=0, y=1), 
    "O": Point(x=-1, y=0)
}

OBJECTS = {
    "pared": walls,
    "bloque": blocks,
    "stickman": stickman,
    "objeto": price
}

def move_robot(robot: Point, direction: str) -> Point:
    """Moves robots

    Arguments:
        robot (Point): Robot position
        direction (str): Robot movement direction

    Returns:
        (Point): Point after robot movement
    """
    new_pos = Point(x=robot.x + MOVS[direction].x, y=robot.y + MOVS[direction].y)
    if 0 <= new_pos.x < WIDTH and 0 <= new_pos.y < HEIGHT:
        return new_pos
    else:
        raise HTTPException(status_code=400, detail="Movement out of bounds")

def perform_action(robot: Point, action: str, objects: List[Object]) -> List[Object]:
    """Performs action

    Arguments:
        robot (Point): Robot position
        action (str): Robot action
        objects (List[Objects]): List of env objects

    Returns:
        (List[Objects]): Objects left after taking action over an object
    """
    target_pos = Point(x=robot.x, y=robot.y - 1) 
    for obj in objects:
        if obj.pos == target_pos:
            obj_info = OBJECTS.get(obj.id, None)
            if obj_info and action in obj_info["allowed_actions"]:
                if action == "D":
                    objects.remove(obj)
                elif action == "M":
                    new_pos = Point(x=obj.pos.x, y=obj.pos.y + 1)
                    if 0 <= new_pos.x < WIDTH and 0 <= new_pos.y < HEIGHT:
                        obj.pos = new_pos
                    else:
                        raise HTTPException(status_code=400, detail="Object movement out of bounds")
                elif action == "R":
                    objects.remove(obj)
                return objects
            else:
                raise HTTPException(status_code=400, detail="Action not allowed on the object")
    raise HTTPException(status_code=400, detail="No object to perform action on")