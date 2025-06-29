from fastapi import Depends
from typing import Optional
from app.infrastructure.database.mongo.orders_repository import OrdersRepository
from app.schemas.order_dto import OrderDTO

class GetOrderUseCase:
    def __init__(self, repo: OrdersRepository):
        self.repo = repo

    async def execute(self, order_id: str) -> Optional[OrderDTO]:
        doc = self.repo.find_by_id(order_id)
        if doc:
            return OrderDTO(**doc)
        return None
