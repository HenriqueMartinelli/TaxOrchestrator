from typing import Protocol, List, Optional
from fastapi import UploadFile, BackgroundTasks
from app.schemas.order_dto import OrderDTO

class OrdersServicePort(Protocol):
    async def process_file(self, file: UploadFile, background_tasks: BackgroundTasks) -> str:
        ...

    async def get_orders(self, status: Optional[str], limit: int) -> List[OrderDTO]:
        ...

    async def get_order(self, order_id: str) -> Optional[OrderDTO]:
        ...
