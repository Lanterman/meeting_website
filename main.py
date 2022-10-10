import os
import uvicorn
from fastapi import FastAPI, status
from starlette.staticfiles import StaticFiles

from config.db import metadata, engine, database, TESTING
from config.utils import LockedError
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


app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(main_router)
app.include_router(websocket_router)

AUTH = ""

# print("Уведомления в websocket: взаимные лайки, добавил в избранное")
# print("create websocket(logic work with db in endpoints, logic work with real time in consumer")

if __name__ == "__main__":

    if TESTING:
        raise LockedError(
            status_code=status.HTTP_423_LOCKED,
            detail="To run the project, you need to set the TESTING variable to False")

    uvicorn.run(app=app, host=os.environ["HOST"], port=int(os.environ["PORT"]))
