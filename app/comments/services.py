from app.comments.repository import CommentsRepository


class CommentsServices:
    def __init__(self, comments_repository: type[CommentsRepository]):
        self.comments_repository: CommentsRepository = comments_repository()

    async def get_list_comments_by_post_id(self, post_id: int):
        return await self.comments_repository.find_all(post_id=post_id)

    async def get_my_comments(self, user_id: int):
        return await self.comments_repository.find_all(user_id=user_id)

    async def create_comment(self, user_id, post_id, text):
        return await self.comments_repository.add(user_id=user_id, post_id=post_id, text=text)

    async def delete_comment(self, user_id, comment_id):
        await self.comments_repository.delete(user_id=user_id, id=comment_id)
