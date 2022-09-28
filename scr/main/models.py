import datetime

import ormar

from config.utils import MainMeta, SEARCH_BY_GENDER
from scr.users.models import Users


class SearchOptions(ormar.Model):
    class Meta(MainMeta):
        tablename = "search_options"

    id: int = ormar.Integer(primary_key=True, index=True)
    search_by_gender: str = ormar.String(max_length=4, choices=SEARCH_BY_GENDER)
    search_by_age_to: int = ormar.Integer(default=10)
    search_by_age_from: int = ormar.Integer(default=20)
    user: int = ormar.ForeignKey(to=Users, ondelete="CASCADE", related_name="search")


class Like(ormar.Model):
    class Meta(MainMeta):
        tablename = "like"

    id: int = ormar.Integer(primary_key=True, index=True)
    data_of_creation: datetime.datetime = ormar.DateTime(default=datetime.datetime.now())
    owner: int = ormar.ForeignKey(to=Users, ondelete="CASCADE", releted_name="owner")
    like: int = ormar.ForeignKey(to=Users, ondelete="CASCADE", related_name="like_set")


class Favorite(ormar.Model):
    class Meta(MainMeta):
        tablename = "favorite"

    id: int = ormar.Integer(primary_key=True, index=True)
    owner: int = ormar.ForeignKey(to=Users, ondelete="CASCADE", releted_name="owner")
    favorite: int = ormar.ForeignKey(to=Users, ondelete="CASCADE", related_name="favorite_set")


class Chat(ormar.Model):
    class Meta(MainMeta):
        tablename = "chat"

    id: int = ormar.Integer(primary_key=True, index=True)
    users: list[Users] = ormar.ManyToMany(to=Users, related_name="chat_set")


class Message(ormar.Model):
    class Meta(MainMeta):
        tablename = "message"

    id: int = ormar.Integer(primary_key=True, index=True)
    message: str = ormar.Text()
    date_of_creation: datetime.datetime = ormar.DateTime(default=datetime.datetime.now())
    chat: int = ormar.ForeignKey(to=Chat, related_name="chat_messages", ondelete="CASCADE")
    owner: int = ormar.ForeignKey(to=Users, related_name="user_messages", ondelete="CASCADE")


class Notification(ormar.Model):
    class Meta(MainMeta):
        tablename = "notification"

    id: int = ormar.Integer(primary_key=True, index=True)
    notification: str = ormar.String(max_length=150)
    is_read: bool = ormar.Boolean(default=False)
    users: list[Users] = ormar.ManyToMany(to=Users, related_name="notification_set")
