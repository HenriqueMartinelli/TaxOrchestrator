from pydantic import BaseModel
from typing import List
from datetime import date

class ProcessResponseDTO(BaseModel):
    message: str

class ItemDTO(BaseModel):
    product_id: str
    quantity: int
    unit_price: float
    ibs_rate: float
    cbs_rate: float
    value_ibs_item: float
    value_cbs_item: float

class OrderDTO(BaseModel):
    order_id: str
    items: List[ItemDTO]
    gross_total: float
    total_ibs: float
    total_cbs: float
    order_total: float
    processing_status: str
    calculation_date: date

class OrderListDTO(BaseModel):
    orders: List[OrderDTO]

class ErrorDTO(BaseModel):
    detail: str
