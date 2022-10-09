import os

from fastapi import APIRouter, Request, BackgroundTasks
from fastapi_sso.sso.google import GoogleSSO
from fastapi.templating import Jinja2Templates

from scr.users import schemas as user_schemas, services as user_services

auth_router = APIRouter(tags=["auth"])
templates = Jinja2Templates(directory="templates")

google_sso = GoogleSSO(os.environ["GOOGLE_CLIENT_ID"], os.environ["GOOGLE_SECRET"], os.environ["GOOGLE_REDIRECT"],
                       allow_insecure_http=True)


@auth_router.get("/", include_in_schema=False)
async def google_login():
    """Generate login url and redirect - endpoint"""

    return await google_sso.get_login_redirect()


@auth_router.get("/google/redirect", response_model=user_schemas.BaseToken, include_in_schema=False)
async def google_redirect(request: Request, back_task: BackgroundTasks):
    """Process login response from Google and return user info - endpoint"""

    user = await google_sso.verify_and_process(request)
    token = await user_services.google_auth(back_task, user.first_name, user.last_name, user.email)
    return token
