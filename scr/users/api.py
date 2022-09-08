from fastapi import APIRouter, HTTPException, status, BackgroundTasks, Depends
from fastapi.security import OAuth2PasswordRequestForm

from config.dependecies import get_current_user
from . import schemas, services, models

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.post("/auth", response_model=schemas.BaseToken)
async def auth(form_data: OAuth2PasswordRequestForm = Depends()):
    """User authenticated - endpoint"""

    user = await services.get_user_by_email(form_data.username)

    if not user:
        HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password!")

    if not services.validate_password(form_data.password, user.password):
        HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password!")

    token = await services.create_user_token(user_id=user.id)
    return token


@user_router.post("/sign-on", response_model=schemas.UserAndHisToken, status_code=status.HTTP_201_CREATED)
async def create_user(form_data: schemas.CreateUser, back_task: BackgroundTasks):
    """Create user - endpoint"""

    user = await services.get_user_by_email(form_data.email)

    if user:
        raise HTTPException(detail="User with this email already exists!", status_code=status.HTTP_400_BAD_REQUEST)

    return await services.create_user(form_data, back_task)


@user_router.delete("/delete_user")
async def delete_user(back_task: BackgroundTasks, current_user: models.Users = Depends(get_current_user)):
    """Delete user - endpoint"""

    user = await services.delete_user(back_task=back_task, user=current_user)
    return {"detail": "Successful!", "user_id": user}
