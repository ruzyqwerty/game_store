from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.orders.router import router as order_router
from src.user.router import router as user_router
from src.product.router import router as product_router
from src.pages.router import router as pages_router
from insert_data import router as insert_data_router

app = FastAPI()

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(order_router)
app.include_router(user_router)
app.include_router(product_router)
app.include_router(pages_router)
app.include_router(insert_data_router)
