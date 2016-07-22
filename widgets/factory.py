from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import sqltypes
from wtforms.validators import Optional, DataRequired

from widgets.array import ArrayWidget
from widgets.binary import BinaryWidget
from widgets.boolean import BooleanWidget
from widgets.datetime import DatetimeWidget
from widgets.float import FloatWidget
from widgets.integer import IntegerWidget
from widgets.json import JSONWidget
from widgets.text import TextWidget


class WidgetFactory:
    MAPPING = {
        sqltypes.DateTime: DatetimeWidget,
        sqltypes.Float: FloatWidget,
        sqltypes.Integer: IntegerWidget,
        sqltypes.Boolean: BooleanWidget,
        sqltypes.LargeBinary: BinaryWidget,
        postgresql.json.JSON: JSONWidget,
        postgresql.base.ARRAY: ArrayWidget,
        sqltypes.NullType: TextWidget
    }

    @staticmethod
    def build(name, meta, model):
        if meta is None:
            return TextWidget(name, meta, model)

        for sqltype, columntype in WidgetFactory.MAPPING.items():
            if isinstance(meta.type, sqltype):
                widget = columntype(name, meta, model)
                # because it's a UnboundField now, you can't simply set the validators
                if "validators" not in widget.field.kwargs:
                    widget.field.kwargs["validators"] = []
                widget.field.kwargs["validators"] += [Optional() if meta.nullable else DataRequired()]
                return widget

        return TextWidget(name, meta, model)
