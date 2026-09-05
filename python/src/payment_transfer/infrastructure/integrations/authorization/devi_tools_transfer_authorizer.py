import httpx

from payment_transfer.domain.transfers.transfer import Transfer


class DeviToolsTransferAuthorizer:
    def __init__(
        self,
        client: httpx.Client,
        base_url: str = "https://util.devi.tools",
    ) -> None:
        self._client = client
        self._base_url = base_url.rstrip("/")

    def authorize(self, transfer: Transfer) -> bool:
        response = self._client.get(
            f"{self._base_url}/api/v2/authorize"
        )

        response.raise_for_status()

        data = response.json()

        return data.get("data", {}).get("authorization", False)
