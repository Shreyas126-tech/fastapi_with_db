from fastapi import APIRouter

router=APIRouter()

@router.post("/users")
def signup():
    return {"message": "User  signed up successfully"}

@router.post("/users/login")
def login():
    return {"message": "User logged in successfully"}

