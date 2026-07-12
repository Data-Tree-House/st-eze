from fastapi import APIRouter

from . import users

router: APIRouter = APIRouter(
    prefix="/v1",
    responses={404: {"description": "Not found"}},
)
router.include_router(users.router)
