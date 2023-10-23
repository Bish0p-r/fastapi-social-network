from sqlalchemy.exc import NoResultFound, IntegrityError

from app.posts.repository import PostsRepository
from app.utils.exceptions import YouAreNotPostAuthorOrIncorrectPostIDException, YouHaveBeenBlackListedException


class PostsServices:
    def __init__(self, posts_repository: type[PostsRepository]):
        self.posts_repository: PostsRepository = posts_repository()

    async def get_list_of_posts(self, author_id=None, **filter_by):
        return await self.posts_repository.get_list_of_posts_with_likes(author_id, **filter_by)

    async def create_post(self, author_id, title, content):
        return await self.posts_repository.add(author_id=author_id, title=title, content=content)

    async def delete_post(self, author_id, post_id):
        await self.posts_repository.delete(author_id=author_id, id=post_id)

    async def partial_update_post(self, author_id, post_id, **data):
        try:
            return await self.posts_repository.partial_update(author_id=author_id, post_id=post_id, **data)
        except NoResultFound:
            raise YouAreNotPostAuthorOrIncorrectPostIDException

    async def check_permission(self, post_id, black_list=None):
        if black_list:
            post = await self.posts_repository.find_by_id(model_id=post_id)
            if post.author_id in black_list:
                raise YouHaveBeenBlackListedException
