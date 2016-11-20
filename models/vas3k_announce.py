from flask import render_template, request

from base.model import BaseAdminModel
from base.view import BaseView
from common.telebot import post_new_story
from db.vas3kru import Vas3kDatabase, Story


class AnnounceAdminModel(BaseAdminModel):
    db = Vas3kDatabase
    table = Story
    name = "announce"
    title = "announce"
    place = "navbar"

    class IndexView(BaseView):
        url = "/"
        title = "Анонс"
        template = "plugins/announce.html"

        def get(self):
            return self.render()

        def post(self):
            text = request.form["text"]
            url = request.form["url"]
            post_new_story(text=text, url=url)
            return render_template("success.html", message="Posted! {} {}".format(text, url))

    list_view = IndexView
