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

from src.app.auto.service import decide_action

from loguru import logger


router = APIRouter(
    prefix="/api/auto",
    tags=["auto"]
)

@router.post("")
def auto(env: AutoEnvRequest) -> EnvResponse:
    """POST method for /auto

    Arguments:
        env (AutoEnvRequest): See more in `src.app.auto.schemas.input`

    Returns:
        (EnvResponse): See more in `src.app.auto.schemas.output`
    """
    robot = env.robot
    env_objects = env.env_objects if env.env_objects else []
    close_objects = env.close_objects if env.close_objects else []
    
    try:
        action = decide_action(robot, env_objects, close_objects)
        return EnvResponse(**action)
    
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e))
    
    