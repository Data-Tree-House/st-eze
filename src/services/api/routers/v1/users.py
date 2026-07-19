from fastapi import (
    APIRouter,
)

router: APIRouter = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def demo_user():
    return "hello"
