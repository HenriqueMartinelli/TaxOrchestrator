from typing import Optional
from app.infrastructure.database.mongo.orders_repository import OrdersRepository
from app.schemas.order_dto import OrderListDTO

class ListOrdersUseCase:
    def __init__(self, repo: OrdersRepository):
        self.repo = repo

    async def execute(self, status: Optional[str], limit: int) -> OrderListDTO:
        docs = self.repo.find_all(status, limit)
        return OrderListDTO(orders=docs)
