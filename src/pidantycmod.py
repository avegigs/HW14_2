import datetime
from typing import Optional
from pydantic import BaseModel, validator


class ContactBase(BaseModel):
    """
    Базова модель для контакту.

    Attributes:
        first_name (str): Ім'я контакту.
        last_name (str): Прізвище контакту.
        email (str): Адреса електронної пошти контакту.
        phone_number (str): Номер телефону контакту.
        birthdate (datetime.date): Дата народження контакту.
        additional_info (str, optional): Додаткова інформація про контакт (необов'язково).
    """
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birthdate: datetime.date
    additional_info: str = None


class ContactCreate(BaseModel):
    """
    Модель для створення нового контакту.

    Attributes:
        first_name (str): Ім'я контакту.
        last_name (str): Прізвище контакту.
        email (str): Адреса електронної пошти контакту.
        phone_number (str): Номер телефону контакту.
        birthdate (str): Дата народження контакту у форматі "dd.mm.yyyy".
        additional_info (str, optional): Додаткова інформація про контакт (необов'язково).

    Methods:
        validate_birthdate_format(cls, value): Метод-валідатор для перевірки формату дати народження.
    """
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birthdate: str
    additional_info: str = None

    @validator("birthdate")
    def validate_birthdate_format(cls, value):
        try:
            parsed_date = datetime.strptime(value, "%d.%m.%Y").date()
            return parsed_date
        except ValueError:
            raise ValueError('Invalid date format. Please use "dd.mm.yyyy" format.')


class ContactResponse(BaseModel):
    """
    Модель відповіді для контакту.

    Attributes:
        first_name (str): Ім'я контакту.
        last_name (str): Прізвище контакту.
        email (str): Адреса електронної пошти контакту.
        phone_number (str): Номер телефону контакту.
        birthdate (datetime.date): Дата народження контакту.
        additional_info (str, optional): Додаткова інформація про контакт (необов'язково).
    """
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birthdate: datetime.date
    additional_info: Optional[str]


class ContactUpdate(ContactBase):
    """
    Модель для оновлення контакту, на основі базової моделі контакту.
    """
    pass


class UserCreate(BaseModel):
    """
    Модель для створення нового користувача.

    Attributes:
        email (str): Адреса електронної пошти користувача.
        password (str): Пароль користувача.
    """
    email: str
    password: str


class UserResponse(BaseModel):
    """
    Модель відповіді для користувача.

    Attributes:
        id (int): Ідентифікатор користувача.
        email (str): Адреса електронної пошти користувача.
    """
    id: int
    email: str


class AvatarResponse(BaseModel):
    """
    Модель відповіді для аватара користувача.

    Attributes:
        avatar_url (str): URL аватара користувача.
    """
    avatar_url: str
