from typing import Optional
from app.infrastructure.database.mongo.orders_repository import OrdersRepository
from app.schemas.order_dto import OrderListDTO
from app.core.logging import logger

class ListOrdersUseCase:
    def __init__(self, repo: OrdersRepository):
        self.repo = repo

    async def execute(self, status: Optional[str], limit: int) -> OrderListDTO:
        logger.info("Listing orders with status: %s, limit: %d", status, limit)
        docs = self.repo.find_all(status, limit)
        if not docs:
            logger.info("No orders found")
            return OrderListDTO(orders=[])
        return OrderListDTO(orders=docs)
