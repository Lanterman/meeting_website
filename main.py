from fastapi import FastAPI

from config.db import metadata, engine, database
from scr.main.api import main_router
from scr.main.websockets_api import websocket_router
from scr.users.api import user_router
from scr.users.auth import auth_router

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
app .include_router(auth_router)
app.include_router(main_router)
app.include_router(websocket_router)

AUTH = ""

print("Уведомления в websocket: взаимные лайки, добавил в избранное")
print("create websocket(logic work with db in endpoints, logic work with real time in consumer")
