from fastapi import APIRouter

from .stock import router as stock_router
from .users import router as user_router

router: APIRouter = APIRouter(
    prefix="/v1",
    responses={404: {"description": "Not found"}},
)
router.include_router(user_router)
router.include_router(stock_router)
