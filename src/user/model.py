"""
Информация о пользователе
"""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from fastapi import APIRouter, Response, Request


class User(BaseModel):
    user_id: UUID = None
    company_id: UUID = None  # foreignkey
    access_token: str = None
    name: str
    last_name: str
    photo: str = None
    email: str
    date_joined: Optional[datetime] = None
    hash_password: str = None
    is_hr: bool

    def get_values_from_cookies(self, request: Request):
        user_id = request.cookies.get("userId")
        company_id = request.cookies.get("company_id")
        access_token = request.cookies.get("access_token")
        name = request.cookies.get("name")
        last_name = request.cookies.get("last_name")
        photo = request.cookies.get("photo")
        email = request.cookies.get("email")
        date_joined = request.cookies.get("date_joined")
        hash_password = request.cookies.get("hash_password")
        is_hr = request.cookies.get("is_hr")
        return self


class Company(BaseModel):
    company_id: UUID = None
    name: str
    employment: str
    website: str = None
    city: str


class Chat(BaseModel):  # анонимный чат
    message_id: UUID = None
    text: str
    sender: UUID = None  # foreignkey
    to: UUID = None  # foreignkey
    time: Optional[datetime] = None


class Recomendations(BaseModel):  # рекомендации в случае выгорания
    id: int  # PK!
    text: str
