from fastapi import APIRouter
from pydantic import BaseModel
from nebula.actions import system_actions

router = APIRouter(prefix="/system")

class SystemRequest(BaseModel):
    command: str  # shutdown, restart

@router.post("/control")
def system_control(req: SystemRequest):
    cmd = req.command.lower()

    if cmd == "shutdown":
        system_actions.shutdown()
    elif cmd == "restart":
        system_actions.restart()
    else:
        return {"status": "error", "message": "Unknown command"}

    return {"status": "ok", "command": cmd}
