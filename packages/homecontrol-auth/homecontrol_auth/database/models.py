
from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import Uuid, String, Boolean, DateTime


class Base(DeclarativeBase):
    pass

class UserInDB(Base):
    """User in the database"""
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    account_type: Mapped[str] = mapped_column(String)
    enabled: Mapped[bool] = mapped_column(Boolean)

class UserSessionInDB(Base):
    """User session in the database"""

    __tablename__ = "user_sessions"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(Uuid, index=True)
    access_token: Mapped[str] = mapped_column(String)
    refresh_token: Mapped[str] = mapped_column(String)
    long_lived: Mapped[bool] = mapped_column(Boolean)
    expiry_time: Mapped[datetime] = mapped_column(DateTime)