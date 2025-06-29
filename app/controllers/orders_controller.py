
from typing import Self, List, Optional
from fastapi import UploadFile, BackgroundTasks

from app.protocols.orders_service import Orders_service
from app.schemas.schemas import Order


class Orders_controller:
    __slots__ = ("service",)

    def __init__(self: Self, service: Orders_service) -> None:
        """
        Recebe a classe de serviço (que implementa Orders_service)
        e instancia o objeto de serviço.
        """
        # ex.: Orders_controller(OrderService)
        self.service = service()

    async def service_process_orders(
        self: Self, file: UploadFile, background_tasks: BackgroundTasks
    ) -> str:
        """
        Recebe o UploadFile e o BackgroundTasks do FastAPI
        e delega ao service o salvamento, enfileiramento
        e retorno de uma mensagem de confirmação.
        """
        return await self.service.process_file(file, background_tasks)

    async def service_get_orders(
        self: Self, status: Optional[str], limit: int
    ) -> List[Order]:
        """
        Busca uma lista de pedidos no banco, opcionalmente filtrando
        por processing_status, e limitando a qtde de resultados.
        """
        return await self.service.get_orders(status, limit)

    async def service_get_order_by_id(
        self: Self, order_id: str
    ) -> Optional[Order]:
        """
        Busca um único pedido pelo order_id.
        Retorna None se não encontrar.
        """
        return await self.service.get_order_by_id(order_id)
