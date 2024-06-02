from fastapi import APIRouter

from src.base import cmc_client

curr_router = APIRouter(
    prefix='/currencies'
)

@curr_router.get('')
async def get_currencies():
    return await cmc_client.get_listings()


@curr_router.get('/{currency_id}')
async def get_currency(currency_id: int):
    return await cmc_client.get_currency(currency_id)
