from fastapi import APIRouter, Request, WebSocket
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from apps.users import models as user_models
from apps.main import services as main_services

websocket_router = APIRouter(prefix="/ws", tags=["ws"])
templates = Jinja2Templates(directory="templates")


@websocket_router.get("/", response_class=HTMLResponse)
async def notification(request: Request):
    """Websocket for notifications"""

    current_user = await user_models.Users.objects.first()
    users = await main_services.get_users(current_user)
    token = await user_models.Token.objects.get_or_none(user=current_user)
    context = {"request": request, "current_user": current_user, "token": token.token, "found_users": users}
    return templates.TemplateResponse(name="base.html", context=context)


@websocket_router.websocket("/notification")
async def send_notification(websocket: WebSocket):
    """Send notification in real life"""

    await websocket.accept()
