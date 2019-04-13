from godmode.widgets.base import BaseWidget


class BitStringWidget(BaseWidget):
    mappings = {
        0: "First bit",
        1: "Second bit"
    }

    def render_details(self, item):
        value = self.render_list(item)
        if not value:
            return "[EMPTY]"

        value = int(value, 2)
        results = []
        bit = 1
        n = 0
        while bit <= value:
            if value & bit:
                results.append(self.mappings.get(n, "Bit %s = 1" % n))
            bit <<= 1
            n += 1
        return ", ".join(results)
