from fastapi import APIRouter, Depends, BackgroundTasks
from typing import Annotated

from ..dependencies import get_token_header, get_query, write_log

router = APIRouter(
    prefix="/back",
    tags=["back"],
    responses={404: {"description": "Not found"}},
)


@router.post("/send-notification/{email}")
async def send_notification(
    email: str, background_tasks: BackgroundTasks, q: Annotated[str, Depends(get_query)]
):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)
    return {"message": "Message sent"}