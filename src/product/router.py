from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.product.models import Product
from src.product.schemas import InsertProduct, ProductsResponse, \
    ProductInfoResponse, PrductChange
from src.product.utils import products_improve_data_output_view

router = APIRouter(
    prefix="/product",
    tags=["Product"]
)


@router.get("/get_product_info", response_model=ProductInfoResponse)
async def get_product_info(
        id_product: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        stmt = (
            select(Product).filter(Product.id_product == id_product))
        res = await session.execute(stmt)
        product = res.scalar()
        data = {
            "id_product": product.id_product,
            "title": product.title,
            "creation_date": product.creation_date.strftime('%Y-%m-%d'),
            "price": product.price,
            "genre": product.genre,
            "vers": product.vers,
            "main_product": product.main_product,
            "login_user": product.login_user,
        }
        return {"status": "success", "data": data}
    except Exception as e:
        await session.rollback()
        return {"status": "Error", "data": str(e)}


@router.get("/get_products", response_model=ProductsResponse)
async def get_products(
        session: AsyncSession = Depends(get_async_session)
):
    try:
        stmt = (select(Product))
        res = await session.execute(stmt)
        products_result = res.scalars()
        answer = products_improve_data_output_view(products_result)
        return {"status": "success", "data": answer}
    except Exception as e:
        await session.rollback()
        return {"status": "Error", "data": str(e)}


@router.post("/create_product", response_model=PrductChange)
async def create_product(
        data: InsertProduct,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        new_product = Product(
            title=data.title,
            price=data.price,
            genre=data.genre,
            vers=data.vers,
            main_product=data.main_product if data.main_product else None,
            login_user=data.login_user,
        )
        session.add(new_product)
        await session.commit()
        return {"status": "success", "message": "New product added"}
    except Exception as e:
        await session.rollback()
        return {"status": "error", "message": str(e)}


@router.delete("/delete_product", response_model=PrductChange)
async def delete_product(
        id_product: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        stmt = (
            select(Product).filter(Product.id_product == id_product))
        res = await session.execute(stmt)
        product = res.scalar()
        if product:
            await session.delete(product)
            await session.commit()
            return {"status": "success", "message": "Product deleted"}
        else:
            return {"status": "error", "message": "Product not found"}
    except Exception as e:
        await session.rollback()
        return {"status": "error", "message": str(e)}
