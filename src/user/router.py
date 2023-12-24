from fastapi import APIRouter, Depends
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.product.models import Product
from src.product.schemas import ProductsResponse
from src.product.utils import products_improve_data_output_view
from src.user.models import User
from src.user.schemas import NewUser, UserInfo, AuthResponse
from src.user.utils import create_token

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/get_user_games", response_model=ProductsResponse)
async def get_user_games(
        login_user: str,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        stmt = (
            select(Product)
            .join(User, Product.login_user == User.login_user)
            .filter(User.login_user == login_user)
        )
        res = await session.execute(stmt)
        user_games = res.scalars()
        answer = products_improve_data_output_view(user_games)
        return {"status": "succes", "data": answer}
    except Exception as e:
        return {"status": "error", "data": str(e)}


@router.post("/auth/login", response_model=AuthResponse)
async def login(
        user_info: UserInfo,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        stmt = (
            select(User)
            .filter(
                User.login_user == user_info.login_user and
                User.password == user_info.password
            )
        )
        res = await session.execute(stmt)
        user = res.fetchone()
        if user:
            token = create_token(user[0].login_user)
            return {"status": "success", "data": token}
        else:
            return {"status": "error", "data": "Invalid Credentials"}
    except Exception as e:
        return {"status": "error", "data": str(e)}


@router.post("/auth/register", response_model=AuthResponse)
async def register(
        data: NewUser,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        new_user = User(
            login_user=data.login_user,
            bill=data.bill,
            password=data.password,
        )
        session.add(new_user)
        await session.commit()
        token = create_token(data.login_user)
        return {"status": "success", "data": token}
    except Exception as e:
        await session.rollback()
        return {"status": "error", "data": str(e)}


@router.put("/top_up_balance", response_model=AuthResponse)
async def top_up_balance(
        login_user: str,
        balance: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        stmt = (
            select(User)
            .filter(
                User.login_user == login_user
            )
        )
        res = await session.execute(stmt)
        user = res.fetchone()
        if user:
            new_balance = balance + user[0].balance
            stmt = (
                update(User)
                .where(User.login_user == login_user)
                .values(
                    {
                        "balance": new_balance
                    }
                )
            )
            await session.execute(stmt)
            await session.commit()
            return {"status": "success", "data": f"New balance: {new_balance}"}
        else:
            return {"status": "error", "data": "Invalid Credentials"}
    except Exception as e:
        await session.rollback()
        return {"status": "error", "data": str(e)}
