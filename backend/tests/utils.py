import random
import string

from typing import Dict
from fastapi.testclient import TestClient
from sqlmodel import Session

from backend.app import settings
from uuid import uuid4

from backend.app.api.services.users import (
    create_user,
    get_user_by_email,
    update_user,
)
from backend.app.models.users import User, UserCreate, UserUpdate

EMAIL_LEN = 5


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=EMAIL_LEN))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def get_superuser_token_headers(client: TestClient) -> Dict[str, str]:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }

    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()

    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers


def user_authentication_headers(
    *, client: TestClient, email: str, password: str
) -> Dict[str, str]:
    data = {"username": email, "password": password}

    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def create_random_user(db: Session) -> User:
    email = random_email()
    password = random_lower_string()
    id_ = uuid4()

    user_in = UserCreate(id=id_, email=email, password=password)
    user = create_user(session=db, user_create=user_in)
    return user


def authentication_token_from_email(
    *, client: TestClient, email: str, db: Session
) -> Dict[str, str]:
    """
    Return a valid token for the user with given email.

    If the user doesn't exist it is created first.
    """
    password = random_lower_string()
    user = get_user_by_email(session=db, email=email)

    if not user:
        id_ = uuid4()
        user_in_create = UserCreate(id=id_, email=email, password=password)
        user = create_user(session=db, user_create=user_in_create)
    else:
        user_in_update = UserUpdate(password=password)
        user = user[0]
        if not user.id:
            raise Exception("User id not set")
        user = update_user(session=db, db_user=user, user_in=user_in_update)

    return user_authentication_headers(client=client, email=email, password=password)
