from fastapi import FastAPI

from config.db import metadata, engine, database
from scr.main.api import main_router
from scr.main.websockets_api import websocket_router
from scr.users.api import user_router

app = FastAPI()

metadata.create_all(engine)
app.state.database = database


@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()


app.include_router(user_router)
app.include_router(main_router)
app.include_router(websocket_router)

AUTH = ""

print("доделать чаты, get_chat_with_email поиск чата по пользователям, schema for chat")
print("придумать что-то со взаимными лайками, выводить уведомления в websocket")
print("Уведомления: взаимные лайки, добавил и убрал из избранных")
print("переделать чат: path attr replace to query attr - two user emails")
