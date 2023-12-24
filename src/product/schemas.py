from datetime import datetime
from typing import Optional, List, Union

from pydantic import BaseModel, Field
from sqlalchemy import null


class ProductBase(BaseModel):
    id_product: int
    title: str
    creation_date: str
    price: float
    genre: str
    vers: float
    main_product: Optional[int]
    login_user: str

class InsertProduct(BaseModel):
    title: str
    price: int
    genre: str
    vers: float
    main_product: Optional[int]
    login_user: str


class ProductsResponse(BaseModel):
    status: str
    data: Optional[List[ProductBase] | str]

class ProductInfoResponse(BaseModel):
    status: str
    data: Optional[ProductBase | str]

class PrductChange(BaseModel):
    status: str
    message: str