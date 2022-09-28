from fastapi import APIRouter, Request, Depends, WebSocket
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from config.dependecies import get_current_user
from scr.users import models as user_models


websocket_router = APIRouter(prefix="/ws", tags=["/ws"])
templates = Jinja2Templates(directory="templates")


@websocket_router.get("/", response_class=HTMLResponse)
async def notification(request: Request):
    """Websocket for notifications"""

    context = {"request": request, "photo_id": 1}
    return templates.TemplateResponse(name="base.html", context=context)


@websocket_router.websocket("/notification")
async def send_notification(websocket: WebSocket):
    """Send notification in real life"""

    await websocket.accept()


async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    current_user = None

    while True:
        data = await websocket.receive_text()
        video_id, username = data.split(", ")

        if not current_user:
            current_user = await services.get_user_by_username(username)

        count_likes = await set_like(int(video_id), current_user)
        await websocket.send_text(f"{count_likes}")