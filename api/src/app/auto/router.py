"""/auto endpoints

Operations:
    - GET
"""

# Third-party imports
from fastapi import APIRouter
from fastapi import HTTPException

# Internal imports
from src.app.auto.schemas.input import AutoEnvRequest
from src.app.auto.schemas.output import EnvResponse

from src.app.auto.service import decide_action_with_gpt4
from src.app.manual.serive import move_robot, perform_action

from src.app.constants import MOVS, ACTIONS


router = APIRouter(
    prefix="/auto",
    tags=["auto"]
)

@router.get("")
def auto(env: AutoEnvRequest) -> EnvResponse:
    """GET method for /auto

    Arguments:
        env (AutoEnvRequest): See more in `src.app.auto.schemas.input`

    Returns:
        (EnvResponse): See more in `src.app.auto.schemas.output`
    """
    robot = env.robot
    objects = env.env_objects if env.env_objects else []
    close_objects = env.close_objects if env.close_objects else []
    
    try:
        action_decision = decide_action_with_gpt4(robot, close_objects)

        if action_decision in MOVS:
            robot = move_robot(robot, action_decision)
        elif action_decision in ACTIONS:
            objects = perform_action(robot, action_decision, objects)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return EnvResponse(robot=robot, objects=objects)