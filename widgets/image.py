from base.widget import BaseWidget


class ImageWidget(BaseWidget):
    filterable = False

    def render_list(self, item):
        value = getattr(item, self.name, None)
        return "<div class='square-img square-img_size_75' style='background-image: url({});'></div>".format(value)
