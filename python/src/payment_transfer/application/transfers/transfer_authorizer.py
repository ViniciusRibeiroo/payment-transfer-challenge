from typing import Protocol

from payment_transfer.domain.transfers.transfer import Transfer


class TransferAuthorizer(Protocol):
    def authorize(self, transfer: Transfer) -> bool:
        ...
