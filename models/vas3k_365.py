from datetime import datetime

import requests
from flask import render_template, request

from base.model import BaseAdminModel
from base.view import BaseView
from common.telebot import post_new_story
from db.vas3kru import Vas3kDatabase, Story


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

            saved_filename = "/tmp/365.{}".format(file.filename[file.filename.rfind(".") + 1:])
            file.save(saved_filename)

            response = requests.post(
                url="http://i.vas3k.ru/upload/",
                files={"image": open(saved_filename, "rb")}
            )

            uploaded_filename = response.json()["url"]

            today_date = datetime.now().strftime("%Y-%m-%d")

            self.model.create(
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

            post_new_story(text="365 project: фотка каждый день", url="http://vas3k.ru/365/{}/".format(today_date))

            return render_template("success.html", message="Saved: <a href='http://vas3k.ru/365/{today}/'>http://vas3k.ru/365/{today}/</a>".format(today=today_date))

    list_view = IndexView
