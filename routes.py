from fastapi import APIRouter
from schemas import UserSignup
from auth import hash_password
from crud import create_user, get_users, update_user, delete_user
from fastapi import status
from auth import verify_password
from schemas import UserLogin
from crud import get_user_by_email
from fastapi import HTTPException,status






router = APIRouter()

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: UserSignup):
    hashed = hash_password(user.password)
    create_user(user, hashed)
    return {"message": "user registered successfully"}


@router.get("/users")
def fetch_users():
    return get_users()


@router.put("/users/{user_id}")
def update(user_id: int, user: UserSignup):
    update_user(user_id, user)
    return {"message": "user updated"}


@router.delete("/users/{user_id}")
def delete(user_id: int):
    delete_user(user_id)
    return {"message": "user deleted"}

@router.post("/login")
def login(user: UserLogin):
    db_user=get_user_by_email(user.email)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid password and email"
        )
    if not verify_password(user.password,db_user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid password or user"
        )
   
   
    return {

        "message":"login successfully",
        "user_id": db_user["id"],
        "email": db_user["email"]
        
        }