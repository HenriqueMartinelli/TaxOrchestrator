from typing import Optional

from app.application.ports.orders_service import OrdersServicePort
from app.schemas.order_dto import (
    ProcessResponseDTO, OrderListDTO, OrderDTO
)
from app.application.usecases.process_orders import ProcessOrdersUseCase
from app.application.usecases.list_orders import ListOrdersUseCase
from app.application.usecases.get_order import GetOrderUseCase

from app.infrastructure.pipeline.excel.excel_reader import ExcelReaderFactory
from app.infrastructure.pipeline.polars.polars_processor import PolarsProcessor
from app.infrastructure.database.mongo.orders_repository import OrdersRepository


class OrdersServiceAdapter(OrdersServicePort):
    async def process_file(self, file, background_tasks):
        usecase = ProcessOrdersUseCase(
            reader_factory=ExcelReaderFactory(),
            processor=PolarsProcessor(),
            repo=OrdersRepository()
        )
        return await usecase.execute(file, background_tasks)

    async def get_orders(self, status: Optional[str], limit: int) -> OrderListDTO:
        usecase = ListOrdersUseCase(
            repo=OrdersRepository()
        )
        return await usecase.execute(status, limit)

    async def get_order(self, order_id: str) -> Optional[OrderDTO]:
        usecase = GetOrderUseCase(
            repo=OrdersRepository()
        )
        return await usecase.execute(order_id)
    


    
