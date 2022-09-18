from fastapi import APIRouter, HTTPException, status, BackgroundTasks, Depends, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm

from config.dependecies import get_current_user
from . import schemas, services, models

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.get("/profile")
async def profile(current_user: models.Users = Depends(get_current_user)):
    """Authorized ser profile - endpoint"""

    return current_user.dict(exclude={"password", "token_set", "secret_key_set", "likes"})


@user_router.post("/auth", response_model=schemas.BaseToken, status_code=status.HTTP_202_ACCEPTED)
async def auth(form_data: OAuth2PasswordRequestForm = Depends()):
    """User authenticated - endpoint"""

    user = await services.get_user_by_email(form_data.username)

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password!")

    if not services.validate_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password!")

    token = await services.create_user_token(user_id=user.id)
    return token


@user_router.post("/sign-on", response_model=schemas.UserAndHisToken, status_code=status.HTTP_201_CREATED)
async def create_user(form_data: schemas.CreateUser, back_task: BackgroundTasks):
    """Create user - endpoint"""

    user = await services.get_user_by_email(form_data.email)

    if user:
        raise HTTPException(detail="User with this email already exists!", status_code=status.HTTP_400_BAD_REQUEST)

    return await services.create_user(form_data, back_task)


@user_router.put("/update_info", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.UpdateUserInfo)
async def update_user_info(form_data: schemas.UpdateUserInfo, current_user: models.Users = Depends(get_current_user)):
    """Update user information - endpoint"""

    check_user = await services.get_user_by_email(form_data.email)

    if check_user and check_user != current_user:
        raise HTTPException(detail="User with this email already exists!", status_code=status.HTTP_400_BAD_REQUEST)

    update_data = await services.update_user_info(form_data, current_user)
    return update_data


@user_router.put("/reset_password", status_code=status.HTTP_202_ACCEPTED)
async def reset_password(form_data: schemas.ResetPassword, current_user: models.Users = Depends(get_current_user)):
    """Reset password - endpoint"""

    if not services.validate_password(form_data.old_password, current_user.password):
        raise HTTPException(detail="Wrong old password!", status_code=status.HTTP_400_BAD_REQUEST)

    await services.reset_password(form_data, current_user)
    return {"detail": "Successful!", "user": schemas.BaseUser(**current_user.dict())}


@user_router.post("/add_photo", status_code=status.HTTP_201_CREATED, response_model=schemas.AddPhoto)
async def add_photo(
        back_task: BackgroundTasks, photo: UploadFile = File(), current_user: models.Users = Depends(get_current_user)
):
    """Add photo - endpoint"""

    path_to_photo = await services.add_photo(back_task, photo, current_user)
    return {"path_to_photo": path_to_photo, "photo": photo}


@user_router.delete("/delete_user")
async def delete_user(back_task: BackgroundTasks, current_user: models.Users = Depends(get_current_user)):
    """Delete user - endpoint"""

    user = await services.delete_user(back_task=back_task, user=current_user)
    return {"detail": "Successful!", "user_id": user}
