from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import HTTPException
from database.models import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: Session, user_id: int):
    """
    Отримання користувача за його ідентифікатором.

    Args:
        db (Session): Об'єкт сесії бази даних.
        user_id (int): Ідентифікатор користувача.

    Returns:
        User: Об'єкт користувача.
    """
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    """
    Отримує користувача з бази даних за адресою електронної пошти.

    Args:
        db (Session): Об'єкт сесії бази даних.
        email (str): Адреса електронної пошти користувача, якого треба отримати.

    Returns:
        User: Об'єкт користувача, якщо користувач існує, в іншому випадку None.
    """
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, email: str, password: str):
    """
    Створює нового користувача та додає його до бази даних.

    Args:
        db (Session): Об'єкт сесії бази даних.
        email (str): Адреса електронної пошти для нового користувача.
        password (str): Пароль для нового користувача.

    Returns:
        User: Об'єкт користувача, який був створений та доданий до бази даних.
    """
    hashed_password = pwd_context.hash(password)
    db_user = User(email=email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str):
    """
    Аутентифікує користувача на основі адреси електронної пошти та пароля.

    Args:
        db (Session): Об'єкт сесії бази даних.
        email (str): Адреса електронної пошти користувача для аутентифікації.
        password (str): Пароль, що вводить користувач для аутентифікації.

    Returns:
        User: Об'єкт користувача, якщо аутентифікація пройшла успішно, в іншому випадку None.
    """
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not pwd_context.verify(password, user.hashed_password):
        return None
    return user
