from fastapi import Request, APIRouter


router = APIRouter(
    prefix="/home",
    tags=["Pages"]
)

@router.get("")
async def home(request: Request):
    return "Home page"

@router.get("/login")
async def login(request: Request):
    return "login page"

@router.get("/register")
async def register(request: Request):
    return "register page"

@router.get("/library")
async def library(request: Request):
    return "library page"

@router.get("/store")
async def store(request: Request):
    return "store page"

@router.get("/basket")
async def basket(request: Request):
    return "basket page"

@router.get("/profile")
async def profile(request: Request):
    return "profile page"

@router.get("/add_product")
async def add_game(request: Request):
    return "add product page"
