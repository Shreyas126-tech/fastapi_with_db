from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from utils.jwt_handler import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user_id(token: str = Depends(oauth2_scheme)):
    print(f"DEBUG: Entering get_current_user_id with token: {token[:15]}...")
    payload = verify_token(token, token_type="access")
    if not payload:
        print(f"DEBUG: Token verification failed for token: {token[:15]}...")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id = payload.get("sub")
    print(f"DEBUG: Token verified. user_id: {user_id}")
    if user_id is None:
        print(f"DEBUG: Token payload missing 'sub'. Payload: {payload}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return int(user_id)
