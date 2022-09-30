from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends

from scr.users import services as user_services
from scr.main import services as main_services


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/auth")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Authenticated user with jwt"""
    token = await user_services.get_user_token(token)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticated": "Bearer"}
        )

    if not token.user.is_activated:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user!")
    token.user.notification_set = await main_services.get_unread_user_notifications(token.user.id)
    return token.user
