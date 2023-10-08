from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
from database.models import User
from fastapi import Depends, HTTPException, status

from database.users import get_user_by_email
from database.database import get_db
import os


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 1440

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


async def create_access_token(data: dict, expires_delta: Optional[float] = None):
    """
    Створює та повертає токен доступу.

    Args:
        data (dict): Дані для створення токена.
        expires_delta (float, optional): Тривалість дії токена в секундах. Defaults to None.

    Returns:
        str: Токен доступу.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + timedelta(seconds=int(expires_delta))
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def create_refresh_token(
    data: dict, db: Session, expires_delta: Optional[float] = None
):
    """
    Створює та повертає токен оновлення.

    Args:
        data (dict): Дані для створення токена.
        db (Session): Об'єкт сесії бази даних.
        expires_delta (float, optional): Тривалість дії токена в секундах. Defaults to None.

    Returns:
        str: Токен оновлення.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + timedelta(seconds=int(expires_delta))
    else:
        expire = datetime.utcnow() + timedelta(minutes=60 * 24)  # 1 день
    to_encode.update({"exp": expire})
    encoded_refresh_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    user = db.query(User).filter(User.email == data["sub"]).first()
    user.refresh_token = encoded_refresh_token
    db.commit()

    return encoded_refresh_token


async def create_access_token_from_refresh_token(refresh_token: str, db: Session):
    """
    Оновлює токен доступу на основі токена оновлення.

    Args:
        refresh_token (str): Токен оновлення.
        db (Session): Об'єкт сесії бази даних.

    Returns:
        dict: Результат оновлення токену доступу.
    """
    login = await get_login_from_refresh_token(refresh_token)
    if login is None:
        raise HTTPException(status_code=401, detail="Refresh token is invalid")

    user = get_user_by_email(db, login)

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires.total_seconds()
    )
    return {"access_token": access_token, "token_type": "bearer"}


async def get_login_from_refresh_token(refresh_token):
    """
    Отримує ім'я користувача з токена оновлення.

    Args:
        refresh_token (str): Токен оновлення.

    Returns:
        str: Ім'я користувача.
    """
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        login = payload.get("sub")
        return login
    except JWTError:
        return None


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """
    Отримує інформацію про поточного користувача на основі токену доступу.

    Args:
        token (str): Токен доступу.
        db (Session): Об'єкт сесії бази даних.

    Returns:
        User: Об'єкт користувача.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token = token.removeprefix("Bearer ")

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload["sub"]
        if email is None:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception

    user: User = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user
