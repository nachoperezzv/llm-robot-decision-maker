"""/manual endpoints

Operations:
    - GET
"""

# Third-party imports
from fastapi import APIRouter
from fastapi import HTTPException

# Internal imports
from src.app.manual.schemas.input import ManualEnvRequest
from src.app.manual.schemas.output import EnvResponse

from src.app.manual.service import move_robot, perform_action

router = APIRouter(
    prefix="/manual",
    tags=["manual"]
)

@router.get("")
def manual(env: ManualEnvRequest) -> EnvResponse:
    """GET method for /manual

    Arguments:
        env (ManualEnvRequest): See more in `src.app.manual.schemas.input`

    Returns:
        (EnvResponse): See more in `src.app.manual.schemas.output`
    """
    if env.mov and env.action:
        raise HTTPException(status_code=400, detail="Cannot send both 'mov' and 'action'")
    
    robot = env.robot
    objects = env.env_objects if env.env_objects else []

    try:
        if env.mov:
            robot = move_robot(env.robot, env.mov)
        elif env.action:
            objects = perform_action(env.robot, env.action, objects)
    except HTTPException as e:
        raise e

    return EnvResponse(robot=robot, objects=objects)