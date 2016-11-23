from collections import defaultdict
from datetime import datetime

import re
import requests
from flask import render_template, request, Markup

from base.model import BaseAdminModel
from base.view import BaseView
from common.telebot import post_new_story
from db.vas3kru import Vas3kDatabase, Story, Comment


class The365AdminModel(BaseAdminModel):
    db = Vas3kDatabase
    table = Story
    name = "365"
    title = "365"
    place = "navbar"

    class IndexView(BaseView):
        url = "/"
        title = "365"
        template = "plugins/365.html"

        def get(self):
            return self.render()

        def post(self):
            file = request.files["photo"]
            if file.filename == "":
                return render_template("error.html", message="No file")

            announce_text = request.form.get("text") or "В эфире программа «дратути». Коротко за сегодня:"

            saved_filename = "/tmp/365.{}".format(file.filename[file.filename.rfind(".") + 1:])
            file.save(saved_filename)

            response = requests.post(
                url="http://i.vas3k.ru/upload/",
                files={"image": open(saved_filename, "rb")}
            )

            uploaded_filename = response.json()["url"]

            today_date = datetime.now().strftime("%Y-%m-%d")

            previous_story = self.model.session.\
                query(Story).\
                filter(Story.type == '365').\
                order_by(Story.created_at.desc()).\
                first()

            new_story = self.model.create(
                slug=today_date,
                type="365",
                title=today_date,
                author="vas3k",
                image=uploaded_filename,
                text="",
                created_at=datetime.now(),
                views_count=0,
                comments_count=0,
                is_visible=True,
                is_commentable=True,
                is_featured=False,
                is_sexy_title=False
            )

            telegram_text = "{}\n\n365 project: http://vas3k.ru/365/{}/".format(announce_text, new_story.slug)

            daily_comments = self.model.session.\
                query(Comment).\
                join(Story, Story.id == Comment.story_id).\
                filter(Comment.created_at > previous_story.created_at).\
                order_by(Comment.block)

            group_comments = defaultdict(list)

            for comment in daily_comments:
                group_comments[comment.story].append(comment)

            for story, comments in group_comments.items():
                telegram_text += "\n\nКомментарии к «{}» http://vas3k.ru/{}/{}/ :".format(story.title, story.type, story.slug)
                for comment in comments:
                    telegram_text += "\n"
                    telegram_text += self.make_comment_text(comment)

            post_new_story(text=telegram_text, with_chat=False)

            return render_template("success.html", message="Saved: <a href='http://vas3k.ru/365/{today}/'>http://vas3k.ru/365/{today}/</a>".format(today=today_date))

        def make_comment_text(self, comment):
            text = Markup(comment.text).striptags()
            text = re.sub(r'^https?:\/\/.*[\r\n]*', '[URL]', text, flags=re.MULTILINE)
            return " {}: {}".format(comment.author, text)

    list_view = IndexView
