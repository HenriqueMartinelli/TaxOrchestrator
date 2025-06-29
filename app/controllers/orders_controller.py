from typing import Optional
from fastapi import UploadFile, BackgroundTasks

from app.application.ports.orders_service import OrdersServicePort
from app.schemas.order_dto import ProcessResponseDTO, OrderListDTO, OrderDTO

class OrdersController:
    """
    Controller que só conhece OrdersServicePort (a abstração).
    """

    def __init__(self, service: OrdersServicePort) -> None:
        self.service = service

    async def process_orders(
        self,
        file: UploadFile,
        background_tasks: BackgroundTasks
    ) -> ProcessResponseDTO:
        return await self.service.process_file(file, background_tasks)

    async def list_orders(
        self,
        status: Optional[str],
        limit: int
    ) -> OrderListDTO:
        return await self.service.get_orders(status, limit)

    async def get_order(
        self,
        order_id: str
    ) -> Optional[OrderDTO]:
        return await self.service.get_order(order_id)
