from decimal import Decimal
from uuid import UUID

from sqlalchemy import Enum, Numeric, String, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from payment_transfer.domain.accounts.account_type import AccountType


class Base(DeclarativeBase):
    pass


class AccountModel(Base):
    __tablename__ = "accounts"

    id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
    )

    full_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    document: Mapped[str] = mapped_column(
        String(14),
        unique=True,
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    account_type: Mapped[AccountType] = mapped_column(
        Enum(AccountType),
        nullable=False,
    )

    balance: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=Decimal("0.00"),
    )
