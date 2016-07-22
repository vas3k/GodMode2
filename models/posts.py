from flask import render_template

from base.delete_view import BaseDeleteView
from base.details_view import BaseDetailsView
from base.list_view import BaseListView
from base.model import BaseAdminModel
from common.acl import ACL
from groups.demo import DemoGroup
from db.demo import Post, DemoDatabase
from widgets.longtext import LongTextWidget


class PostsAdminModel(BaseAdminModel):
    acl = ACL.MODERATOR
    db = DemoDatabase
    name = "posts"
    title = "Posts"
    icon = "icon-invoice"
    group = DemoGroup
    index = 10
    table = Post
    widgets = {
        "body": LongTextWidget,
    }

    class PostsListView(BaseListView):
        acl = ACL.MODERATOR
        max_offset = {
            ACL.MODERATOR: 10000
        }
        max_limit = {
            ACL.MODERATOR: 10000
        }
        fields = [
            "id",
            "user_id",
            "title",
            "created_at"
        ]
        default_sorting = Post.created_at.desc()

    list_view = PostsListView

    class PostDetailsView(BaseDetailsView):
        template = "views/post_details.html"
        acl = ACL.MODERATOR

        def get(self, id):
            post = self.model.get(id=id)
            if not post:
                return render_template("error.html", message="Looks like this post does not exist.")
            author = post.user  # just for example
            return self.render(post=post, author=author)

    details_view = PostDetailsView

    class PostsDeleteView(BaseDeleteView):
        acl = ACL.ADMIN

    delete_view = PostsDeleteView

    def after_update(self, old_item, new_item):
        self.session.execute(
                "update users set post_count = (select count(*) from posts where user_id = users.id) where id = :user_id",
                {"user_id": new_item.user_id}
        )
        self.session.execute(
                "update users set post_count = (select count(*) from posts where user_id = users.id) where id = :user_id",
                {"user_id": old_item.user_id}
        )
        self.session.commit()

    def after_create(self, item):
        self.session.execute(
                "update users set post_count = (select count(*) from posts where user_id = users.id) where id = :user_id",
                {"user_id": item.user_id}
        )
        self.session.commit()

    def before_delete(self, item):
        self.session.execute(
                "update users set post_count = (select count(*) from posts where user_id = users.id) where id = :user_id",
                {"user_id": item.user_id}
        )
        self.session.commit()
