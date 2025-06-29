from typing import Protocol, List, Optional
from fastapi import UploadFile, BackgroundTasks

from app.schemas.schemas import Order

class OrdersService(Protocol):
    """
    Protocolo (interface) para serviços de orders.
    Qualquer implementação deve obedecer a estas assinaturas.
    """

    async def process_file(
        self,
        file: UploadFile,
        background_tasks: BackgroundTasks
    ) -> str:
        """
        Recebe o arquivo Excel e o BackgroundTasks do FastAPI,
        deve:
         1. Salvar o arquivo em storage temporário
         2. Enfileirar/processar em background
         3. Retornar mensagem de confirmação
        """

    async def get_orders(
        self,
        status: Optional[str],
        limit: int
    ) -> List[Order]:
        """
        Retorna uma lista de pedidos, podendo filtrar por
        processing_status (status) e limitando a qtde.
        """

    async def get_order_by_id(
        self,
        order_id: str
    ) -> Optional[Order]:
        """
        Retorna um pedido específico pelo seu ID,
        ou None se não encontrado.
        """
