from datetime import datetime

from sqlalchemy import DateTime, Integer, LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column

from database.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    full_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    id_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    id_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    dob: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    gender: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    address: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )

    face_embedding: Mapped[bytes] = mapped_column(
        LargeBinary,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )
