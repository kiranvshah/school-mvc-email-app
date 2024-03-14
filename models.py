from sqlalchemy import Column, Integer, String, Table, ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, relationship, validates
import re
import hashlib


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'emails'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String)

    def __repr__(self):
        return f'EmailAddress(email=\'{self.email}\')'

    @classmethod
    def hash_password(cls, password, email):
        return hashlib.sha256(str.encode(password + email)).hexdigest()

    def set_password(self, password, email):
        self.password_hash = self.hash_password(password, email)

    @validates('email')
    def validate_email(self, key, address):
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(pattern, address):
            raise ValueError('Invalid email address')
        if key != 'email':
            raise ValueError('Key must be \'email\'')
        return address

    @classmethod
    def validate_password(cls, password):
        if len(password) < 8:
            raise ValueError('Password must be at least 8 characters')
        if password.isalnum():
            raise ValueError('Password must contain at least one special character')
        if not any(char.isupper() for char in password):
            raise ValueError('Password must contain at least one capital letter')
        if not any(char.islower() for char in password):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(char.isdigit() for char in password):
            raise ValueError('Password must contain at least one number')
        return password
