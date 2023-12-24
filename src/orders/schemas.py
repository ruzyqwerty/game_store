from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel


class Order(BaseModel):
    id_product: int
    login_user: str
    final_price: int
    trans_datetime: str


class GetOrdersResponse(BaseModel):
    status: str
    message: Optional[str]
    data: Optional[List[Order]]


class NewOrder(BaseModel):
    id_product: int
    login_user: str
    final_price: int