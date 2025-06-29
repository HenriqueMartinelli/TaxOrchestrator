from dataclasses import dataclass
from typing import List
from schemas.money import Money

@dataclass
class Item:
    product_id: str
    quantity: int
    unit_price: Money
    ibs_rate: float
    cbs_rate: float
    value_ibs_item: Money
    value_cbs_item: Money

@dataclass
class Order:
    order_id: str
    items: List[Item]
    gross_total: Money
    total_ibs: Money
    total_cbs: Money
    order_total: Money
    processing_status: str
    calculation_date: str  
