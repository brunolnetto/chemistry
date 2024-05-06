from fastapi import Depends
from typing import Annotated

from src.services.users import UserService

def get_user_service() -> UserService:
    return UserService()

UserServiceDependency = Annotated[UserService, Depends(get_user_service)]
