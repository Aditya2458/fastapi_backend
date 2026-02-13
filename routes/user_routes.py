from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from auth import verify_token
from crud import get_users, update_user, delete_user
from schemas import UserSignup

router = APIRouter(prefix="/api/users", tags=["Users"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


@router.get("/")
def list_users(token: str = Depends(oauth2_scheme)):
    verify_token(token)
    return get_users()


@router.put("/{user_id}")
def update(user_id: int, user: UserSignup, token: str = Depends(oauth2_scheme)):
    verify_token(token)
    update_user(user_id, user)
    return {"message": "User updated"}


@router.delete("/{user_id}")
def delete(user_id: int, token: str = Depends(oauth2_scheme)):
    verify_token(token)
    delete_user(user_id)
    return {"message": "User deleted"}