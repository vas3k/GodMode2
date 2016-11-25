from collections import defaultdict
from datetime import datetime

import re
import requests
from flask import render_template, request, Markup

from base.model import BaseAdminModel
from base.view import BaseView
from common.telebot import post_new_story
from db.vas3kru import Vas3kDatabase, Story, Comment


DEFAULT_ANNOUNCE_TEXT = "В эфире программа «дратути». Коротко за сегодня:"


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

            announce_text = request.form.get("text")

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
                text=announce_text or "",
                created_at=datetime.now(),
                views_count=0,
                comments_count=0,
                is_visible=True,
                is_commentable=True,
                is_featured=False,
                is_sexy_title=False
            )

            telegram_text = "{}\n\nФотка дня: http://vas3k.ru/365/{}/\n".format(announce_text or DEFAULT_ANNOUNCE_TEXT, new_story.slug)

            daily_comments = self.model.session.\
                query(Comment).\
                join(Story, Story.id == Comment.story_id).\
                filter(Comment.created_at > previous_story.created_at).\
                order_by(Comment.block)

            if daily_comments:
                telegram_text += "\nА еще сегодня:"
                group_comments = defaultdict(list)

                for comment in daily_comments:
                    group_comments[comment.story].append(comment)

                for story, comments in group_comments.items():
                    telegram_text += "\n{} к посту «{}» http://vas3k.ru/{}/{}/".format(self.pluralize_comments(len(comments)), story.title, story.type, story.slug)
                    # for comment in comments:
                    #     telegram_text += "\n"
                    #     telegram_text += self.make_comment_text(comment)

            post_new_story(text=telegram_text, with_chat=False)

            return render_template("success.html", message="Saved: <a href='http://vas3k.ru/365/{today}/'>http://vas3k.ru/365/{today}/</a>".format(today=today_date))

        def make_comment_text(self, comment):
            text = Markup(comment.text).striptags()
            text = re.sub(r'^https?:\/\/.*[\r\n]*', '[URL]', text, flags=re.MULTILINE)
            return " {}: {}".format(comment.author, text)

        def pluralize_comments(self, value):
            args = ["{} новый комментарий", "{} новых комментария", "{} новых комментариев"]
            number = abs(int(value))
            a = number % 10
            b = number % 100

            if (a == 1) and (b != 11):
                return args[0].format(value)
            elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
                return args[1].format(value)
            else:
                return args[2].format(value)

    list_view = IndexView
