from fastapi import APIRouter

from app.auth.dependencies import GetCurrentUser

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


@router.get("/list")
async def get_list_of_posts(
):
    pass


@router.post("/create")
async def create_post(
    user=GetCurrentUser,
):
    pass


@router.delete("/delete")
async def delete_post(
    user=GetCurrentUser,
):
    pass

