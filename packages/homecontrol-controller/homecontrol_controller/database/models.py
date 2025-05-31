from uuid import UUID, uuid4

from sqlalchemy import BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import String, Uuid


class Base(DeclarativeBase):
    pass


class ACDeviceInDB(Base):
    """AC device in the database"""

    __tablename__ = "ac_devices"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    ip_address: Mapped[str] = mapped_column(String, unique=True)
    identifier: Mapped[int] = mapped_column(BigInteger)
    key: Mapped[str] = mapped_column(String)
    token: Mapped[str] = mapped_column(String)
