from fastapi import APIRouter, Depends, HTTPException, status

from payment_transfer.api.dependencies import get_transfer_money
from payment_transfer.application.transfers.transfer_money import TransferMoney
from payment_transfer.application.transfers.transfer_request import TransferRequest
from payment_transfer.application.transfers.transfer_response import TransferResponse

router = APIRouter(
    prefix="/transfers",
    tags=["transfers"],
)


@router.post(
    "",
    response_model=TransferResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_transfer(
    request: TransferRequest,
    transfer_money: TransferMoney = Depends(get_transfer_money),
) -> TransferResponse:
    try:
        transfer = transfer_money.execute(
            payer_id=request.payer_id,
            payee_id=request.payee_id,
            amount=request.amount,
        )
    except ValueError as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exception),
        ) from exception

    return TransferResponse(
        id=transfer.id,
        payer_id=transfer.payer_id,
        payee_id=transfer.payee_id,
        amount=transfer.amount,
    )
