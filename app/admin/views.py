from sqladmin import ModelView

from app.users.models import Users
from app.posts.models import Posts
from app.comments.models import Comment
from app.likes.models import Like
from app.blacklist.models import Blacklist
from app.friendships.models import Friendships


class UsersAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email]
    column_details_exclude_list = [Users.hashed_password]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"


class PostsAdmin(ModelView, model=Posts):
    column_list = [Posts.id, Posts.author_id]
    can_delete = True
    name = "Пост"
    name_plural = "Посты"
    icon = "fa-solid fa-align-left"


class CommentsAdmin(ModelView, model=Comment):
    column_list = [Comment.id, Comment.user_id, Comment.post_id]
    can_delete = True
    name = "Комментарий"
    name_plural = "Комментарии"
    icon = "fa-solid fa-comment"


class LikesAdmin(ModelView, model=Like):
    column_list = [Like.id, Like.user_id, Like.post_id]
    can_delete = True
    name = "Лайк"
    name_plural = "Лайки"
    icon = "fa-solid fa-heart"


class FriendshipsAdmin(ModelView, model=Friendships):
    column_list = [Friendships.id, Friendships.from_user, Friendships.to_user]
    can_delete = True
    name = "Друзья"
    name_plural = "Друзья"
    icon = "fa-solid fa-user-group"


class BlacklistsAdmin(ModelView, model=Blacklist):
    column_list = [Blacklist.id, Blacklist.initiator_user, Blacklist.blocked_user]
    can_delete = True
    name = "Черный список"
    name_plural = "Черные списки"
    icon = "fa-solid fa-user-slash"
