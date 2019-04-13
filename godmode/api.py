import hashlib
import json
import re
from time import time

from godmode.exceptions import BadParams


class API:
    @staticmethod
    def useragent(request):
        return request.headers.get("User-Agent", "")

    @staticmethod
    def ipaddress(request):
        return request.headers.get("X-Forwarded-For") or request.headers.get("X-Real-IP") or request.remote_ip

    @staticmethod
    def generate_hash(data=""):
        data = "%s%s" % (str(time()), data)
        return hashlib.md5(data.encode("utf-8")).hexdigest()

    @staticmethod
    def get(request, key, required):
        val = request.args.get(key) or request.form.get(key) or request.cookies.get(key)
        if val is None:
            if required:
                raise BadParams(key)
            else:
                return None
        return val

    @staticmethod
    def __test_variant(key, val, variants):
        if variants and not val in variants:
            raise BadParams(key)

    @staticmethod
    def __test_length(key, val, min, max):
        if len(val) < min or len(val) > max:
            raise BadParams(key)

    @staticmethod
    def get_str(request, key, required=True, variants=None, min=0, max=1000,
                notags=False, forced=False):
        """ Checks extra conditions for a string arg
        """
        val = API.get(request, key, required)

        if val is None:
            return None

        if notags:
            val = strip_tags(val)
            val = re.sub(r"<[\w]+", "", val)

        val = val.strip()

        if forced:
            if None != variants and len(variants) and not val in variants:
                val = variants[0]

            if len(val) > max:
                val = val[:max]

        API.__test_variant(key, val, variants)
        API.__test_length(key, val, min, max)
        return val

    @staticmethod
    def get_str_arr(request, key, required=True, variants=None, min=0, max=1000):
        val = API.get(request, key, required)
        if val is None:
            return None

        vals = val.split(",")
        vals = [val.strip() for val in vals]

        for val in vals:
            API.__test_variant(key, val, variants)
            API.__test_length(key, val, min, max)
        return vals

    @staticmethod
    def get_str_regex(request, key, regex=None, **kwargs):
        name = API.get_str(request, key, **kwargs)
        if regex and not re.match(regex, name):
            raise BadParams(key)
        return name

    @staticmethod
    def get_int_arr(request, key, required=True, variants=None):
        val = API.get(request, key, required)
        if val is None:
            return None

        try:
            vals = map(int, val.split(","))
        except Exception:
            raise BadParams(key)

        for val in vals:
            API.__test_variant(key, val, variants)
        return vals

    @staticmethod
    def get_bool(request, key, required=True):
        val = API.get(request, key, required)
        if val is None:
            return None

        if val in [b"0", b"false", b"False"]:
            return False
        elif val in [b"1", b"true", b"True"]:
            return True
        else:
            raise BadParams(key)

    @staticmethod
    def get_int(request, key, required=True, variants=None, min=None, max=None,
                forced=False):
        """ Checks extra conditions for an int arg
        """
        val = API.get(request, key, required)
        if val is None:
            return None

        try:
            val = int(val)
        except Exception:
            raise BadParams(key)

        if (max is not None) and val > max:
            if forced:
                val = max
            else:
                raise BadParams("%s > %s" % (key, max))

        if (min is not None) and val < min:
            if forced:
                val = min
            else:
                raise BadParams("%s < %s" % (key, min))

        if variants and forced and len(variants) and not val in variants:
            val = variants[0]

        API.__test_variant(key, val, variants)

        return val

    @staticmethod
    def get_float(request, key, required=True):
        val = API.get(request, key, required)
        if val is None:
            return None

        try:
            val = float(val)
        except ValueError:
            raise BadParams(key)

        return val

    @staticmethod
    def get_json(request, key, required=True):
        val = API.get(request, key, required)
        if val is None:
            return None

        try:
            val = json.loads(val.decode('utf8'))
        except:
            raise BadParams(key)

        return val

    @staticmethod
    def get_email(request, key, required=True):
        val = API.get_str(request, key, required, min=3, max=64)
        if val is None:
            return None

        if "@" not in val:
            raise BadParams("Bad email")

        return val.lower()


def strip_tags(text):
    regexp = re.compile(r"<[^>]*?>", re.IGNORECASE)
    return regexp.sub("", text)


def join_url(args):
    url = "/{}/".format("/".join([str(arg or "") for arg in args]))
    url = re.sub("/+", "/", url)
    return url


def try_to_float(value, default=0.0):
    try:
        return float(value)
    except ValueError:
        return default
