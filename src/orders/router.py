from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.orders.models import Transaction
from src.orders.schemas import Order, GetOrdersResponse, NewOrder
from src.orders.utils import orders_improve_data_output_view
from src.user.models import User

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.get("/get_orders", response_model=GetOrdersResponse)
async def get_orders(
        login_user: str,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        user_check = await session.execute(
            select(User).filter(User.login_user == login_user))
        if not user_check.scalar():
            return {
                "status": "erorr",
                "message": "No user with that username",
                "data": None
            }
        stmt = (
            select(Transaction).
            filter(Transaction.login_user == login_user)
        )
        res_query = await session.execute(stmt)
        transactions = res_query.scalars()
        answer = orders_improve_data_output_view(transactions)
        return {
            "status": "success",
            "message": "All orders",
            "data": answer
        }
    except Exception as e:
        return {
            "status": "erorr",
            "message": str(e),
            "data": None
        }


@router.post("/buy_game")
async def buy_game(
        data: NewOrder,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        new_order = Transaction(
            id_product=data.id_product,
            login_user=data.login_user,
            final_price=data.final_price
        )
        session.add(new_order)
        await session.commit()
        return {"status": "Success", "message": "Order"}
    except Exception as e:
        return {"status": "Error", "message": str(e)}
