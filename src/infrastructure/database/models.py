"""SQLAlchemy database models."""
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    Integer,
    MetaData,
    String,
    Table,
    Text,
)


metadata = MetaData()

users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("social_id", BigInteger, unique=True, nullable=False, index=True),
    Column("username", String(32), nullable=True, index=True),
    Column("registration_date", DateTime, nullable=False, default=datetime.utcnow),
    Column("name", Text, nullable=True),
    Column("info", Text, nullable=True),
    Column("photo_file_id", Text, nullable=True),
    Column("taps", BigInteger, nullable=False, default=0, index=True),
) 