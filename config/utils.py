import ormar

from .db import metadata, database


class MainMeta(ormar.ModelMeta):
    metadata = metadata
    database = database

