from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.orders.models import Transaction
from src.product.models import Product
from src.user.models import User

fake_users = [
    {"login_user": "john_doe", "bill": 500, "password": "password123"},
    {"login_user": "alice_smith", "bill": 700, "password": "qwerty456"},
    {"login_user": "bob_jackson", "bill": 300, "password": "passphrase789"},
    {"login_user": "emma_jones", "bill": 800, "password": "securepassword"},
    {"login_user": "mike_wilson", "bill": 400, "password": "myp@ssw0rd"}
]

fake_products = [
    {"title": "Game 1", "price": 50, "genre": "Action", "vers": 1.0, "main_product": None, "login_user": "john_doe"},
    {"title": "Game 2", "price": 30, "genre": "Adventure", "vers": 2.5, "main_product": 1, "login_user": "john_doe"},
    {"title": "Game 3", "price": 40, "genre": "RPG", "vers": 1.8, "main_product": None, "login_user": "john_doe"},
    {"title": "Game 4", "price": 60, "genre": "Strategy", "vers": 3.2, "main_product": None, "login_user": "emma_jones"},
    {"title": "Game 5", "price": 55, "genre": "Sports", "vers": 1.5, "main_product": None, "login_user": "mike_wilson"}
]

fake_orders = [
    {"id_product": 1, "login_user": "john_doe", "final_price": 50},
    {"id_product": 2, "login_user": "alice_smith", "final_price": 30},
    {"id_product": 3, "login_user": "bob_jackson", "final_price": 40},
    {"id_product": 4, "login_user": "emma_jones", "final_price": 60},
    {"id_product": 5, "login_user": "mike_wilson", "final_price": 55}
]

async def insert_product(
        data,
        session
):
    try:
        new_product = Product(
            title=data["title"],
            price=data["price"],
            genre=data["genre"],
            vers=data["vers"],
            main_product=data["main_product"] if data["main_product"]
        else None,
            login_user=data["login_user"],
        )
        session.add(new_product)
        await session.commit()
    except Exception as e:
        await session.rollback()

async def insert_user(
        data,
        session
):
    try:
        new_user = User(
            login_user=data["login_user"],
            bill=data["bill"],
            password=data["password"],
        )
        session.add(new_user)
        await session.commit()
    except Exception as e:
        await session.rollback()

async def insert_order(
        data,
        session
):
    try:
        new_order = Transaction(
            id_product=data["id_product"],
            login_user=data["login_user"],
            final_price=data["final_price"]
        )
        session.add(new_order)
        await session.commit()
    except Exception as e:
        await session.rollback()


async def insert_data(session):
    try:
        for fake_user in fake_users:
            await insert_user(fake_user, session)
        for fake_product in fake_products:
            await insert_product(fake_product, session)
        for fake_order in fake_orders:
            await insert_order(fake_order, session)
        return True
    except Exception as e:
        await session.rollback()
        return False

router = APIRouter(
    prefix="/insert_data",
    tags=["insert_data"]
)

@router.post("/insert_data")
async def route_insert_data(
        session: AsyncSession = Depends(get_async_session)
):
    result = await insert_data(session)
    return result
