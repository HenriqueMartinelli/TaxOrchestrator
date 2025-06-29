from fastapi import APIRouter, Depends, UploadFile, BackgroundTasks, HTTPException, Query
from http import HTTPStatus
from typing import Optional

from app.controllers.orders_controller import OrdersController
from app.services.orders_service_adapter import OrdersServiceAdapter
from app.schemas.order_dto import ProcessResponseDTO, OrderListDTO, OrderDTO, ErrorDTO
from app.shared.exceptions import SchemaValidationError, DataPreparationError

router = APIRouter(prefix="/api/v1/orders", tags=["orders"])

def get_orders_controller() -> OrdersController:
    return OrdersController(OrdersServiceAdapter())

@router.post(
    "/process",
    response_model=ProcessResponseDTO,
    status_code=HTTPStatus.ACCEPTED,
    summary="Upload de Excel e processamento"
)
async def process_orders(
    file: UploadFile,
    background_tasks: BackgroundTasks,
    ctrl: OrdersController = Depends(get_orders_controller),
):
    try:
        return await ctrl.process_orders(file, background_tasks)
    except SchemaValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DataPreparationError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get(
    "/",
    response_model=OrderListDTO,
    status_code=HTTPStatus.OK,
    summary="Listar pedidos"
)
async def list_orders(
    status: Optional[str] = Query(None, description="Filtro por status"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo de registros"),
    ctrl: OrdersController = Depends(get_orders_controller),
):
    return await ctrl.list_orders(status, limit)

@router.get(
    "/{order_id}",
    response_model=OrderDTO,
    status_code=HTTPStatus.OK,
    responses={HTTPStatus.NOT_FOUND: {"model": ErrorDTO}},
    summary="Obter pedido por ID"
)
async def get_order(
    order_id: str,
    ctrl: OrdersController = Depends(get_orders_controller),
):
    order = await ctrl.get_order(order_id)
    if not order:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="Order not found")
    return order
