# app/schemas.py
from typing import List
from datetime import date
from pydantic import BaseModel

class ProcessResponse(BaseModel):
    message: str

class Item(BaseModel):
    product_id: str
    quantity: int
    unit_price: float
    ibs_rate: float
    cbs_rate: float
    value_ibs_item: float
    value_cbs_item: float

class Order(BaseModel):
    order_id: str
    items: List[Item]
    gross_total: float
    total_ibs: float
    total_cbs: float
    order_total: float
    processing_status: str
    calculation_date: date

class OrderListOutput(BaseModel):
    orders: List[Order]

class ErrorMessage(BaseModel):
    detail: str
