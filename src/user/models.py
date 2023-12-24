from sqlalchemy import Column, Integer, String, CheckConstraint, Table
from sqlalchemy.sql import text

from src.database import Base, metadata


class User(Base):
    __tablename__ = 'User'
    metadata = metadata

    login_user = Column(String(50), primary_key=True, nullable=False)
    bill = Column(Integer, nullable=False)
    password = Column(String(50), nullable=False)
    balance = Column(Integer, nullable=False, default=0)
    user_role = Column(String, nullable=False, server_default='user')

    __table_args__ = (
        CheckConstraint(
            text("LENGTH(login_user) >= 5"),
            name='check_login_length'
        ),
        CheckConstraint(
            text("LENGTH(password) >= 5"),
            name='check_password_length'
        ),
        CheckConstraint(
            text("user_role IN ('user', 'creator', 'admin')"),
            name='check_user_role')
    )
