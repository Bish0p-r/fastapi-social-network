from fastapi import APIRouter, Depends, status


router = APIRouter(
    prefix="/blacklist",
    tags=["Blacklist"],
)


@router.get("")
async def test():
    pass

