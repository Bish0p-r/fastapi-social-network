from app.posts.repository import PostsRepository


class PostsServices:
    def __init__(self, posts_repository: type[PostsRepository]):
        self.posts_repository: PostsRepository = posts_repository()

    async def get_list_of_posts(self):
        return await self.posts_repository.find_all()

    async def create_post(self, author_id, title, content):
        return await self.posts_repository.add(author_id=author_id, title=title, content=content)

    async def delete_post(self, author_id, post_id):
        await self.posts_repository.delete(author_id=author_id, id=post_id)
