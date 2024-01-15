from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.schema.authenticate import JWTPAYLOAD

from ..environment_vars import JWT_SECRET, TOKEN_EXPIRY_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

algorithm = "HS256"
secret_key = JWT_SECRET
expiry_minutes = TOKEN_EXPIRY_MINUTES


def generate_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expiry_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    if not token.startswith("Bearer"):
        raise credentials_exception

    split_token = token.split()
    if len(split_token) != 2:
        raise credentials_exception

    try:
        payload = jwt.decode(split_token[1], secret_key, algorithm)
        print("Payload", payload)
        token_data = JWTPAYLOAD(id=payload.get("id"), email=payload.get("email"))
        print("TOken data", token_data)
        return token_data
    except JWTError:
        raise credentials_exception


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not verify credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return verify_access_token(token, credentials_exception)
