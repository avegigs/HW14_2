# database/models.py
from sqlalchemy import Boolean, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Contact(Base):
    """
    Модель бази даних для контактів.

    Attributes:
        id (int): Унікальний ідентифікатор контакту.
        first_name (str): Ім'я контакту.
        last_name (str): Прізвище контакту.
        email (str): Email контакту.
        phone_number (str): Номер телефону контакту.
        birthdate (Date): День народження контакту.
        additional_info (str): Додаткова інформація про контакт.

    Relationships:
        user_email (str): Email користувача, якому належить контакт.
        user (User): Зв'язок із моделлю користувача.
    """
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, unique=True)
    birthdate = Column(Date)
    additional_info = Column(String, nullable=True)
    
    user_email = Column(String, ForeignKey("users.email"))
    user = relationship("User", back_populates="contacts")


class User(Base):
    """
    Модель бази даних для користувачів.

    Attributes:
        id (int): Унікальний ідентифікатор користувача.
        email (str): Email користувача.
        hashed_password (str): Хеш паролю користувача.
        refresh_token (str): Токен оновлення для користувача.
        is_verified (bool): Прапорець, що позначає, чи підтверджено електронну пошту користувача.
        avatar_url (str): URL-адреса аватара користувача.

    Relationships:
        contacts (List[Contact]): Зв'язок із моделлю контактів.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    refresh_token = Column(String, nullable=True, index=True)
    is_verified = Column(Boolean, default=False)
    avatar_url = Column(String, nullable=True)

    contacts = relationship("Contact", back_populates="user")
