from payment_transfer.domain.accounts.account import Account
from payment_transfer.infrastructure.database.models import AccountModel


def to_model(account: Account) -> AccountModel:
    return AccountModel(
        id=account.id,
        full_name=account.full_name,
        document=account.document,
        email=account.email,
        password_hash=account.password_hash,
        account_type=account.account_type,
        balance=account.balance,
    )


def to_domain(model: AccountModel) -> Account:
    return Account(
        account_id=model.id,
        full_name=model.full_name,
        document=model.document,
        email=model.email,
        password_hash=model.password_hash,
        account_type=model.account_type,
        balance=model.balance,
    )
