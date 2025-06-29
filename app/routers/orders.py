from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException, Query
from pydantic import PositiveInt

from app.controllers.orders_controller import OrdersController
from app.services.order_service import OrderService
from app.schemas.schemas import (
    ProcessResponse,
    Order,
    OrderListOutput,
    ErrorMessage,
)

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)

# Instancia o controller apenas uma vez, passando a implementação concreta do service
_orders_ctrl = OrdersController(OrderService)


@router.post(
    "/process",
    response_model=ProcessResponse,
    status_code=HTTPStatus.ACCEPTED,
    summary="Upload de Excel e início do processamento",
    responses={
        HTTPStatus.BAD_REQUEST: {
            "description": "Arquivo inválido",
            "model": ErrorMessage,
        }
    },
)
async def process_orders(
    file: UploadFile = File(..., description="Arquivo .xls ou .xlsx com os pedidos"),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    """
    - Valida extensão do arquivo.
    - Salva temporariamente e dispara o processamento em background.
    """
    filename = file.filename.lower()
    if not (filename.endswith(".xls") or filename.endswith(".xlsx")):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Somente arquivos .xls ou .xlsx são permitidos",
        )

    message = await _orders_ctrl.service_process_orders(file, background_tasks)
    return ProcessResponse(message=message)


@router.get(
    "/",
    response_model=OrderListOutput,
    summary="Lista pedidos; aceita filtro por status",
    responses={
        HTTPStatus.BAD_REQUEST: {
            "description": "Parâmetros de consulta inválidos",
            "model": ErrorMessage,
        }
    },
)
async def read_orders(
    status: Optional[str] = Query(
        None, description="Filtra por processing_status (ex: PROCESSED)"
    ),
    limit: PositiveInt = Query(
        100, ge=1, le=1000, description="Máximo de pedidos retornados"
    ),
):
    """
    Retorna até `limit` pedidos; se `status` for passado,
    retorna apenas aqueles com esse processing_status.
    """
    orders = await _orders_ctrl.service_get_orders(status=status, limit=limit)
    return OrderListOutput(orders=orders)


@router.get(
    "/{order_id}",
    response_model=Order,
    summary="Consulta um pedido pelo seu ID",
    responses={
        HTTPStatus.NOT_FOUND: {
            "description": "Pedido não encontrado",
            "model": ErrorMessage,
        }
    },
)
async def read_order(order_id: str):
    """
    Busca no banco o pedido com este `order_id`.
    """
    order = await _orders_ctrl.service_get_order_by_id(order_id)
    if not order:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Pedido não encontrado",
        )
    return order
