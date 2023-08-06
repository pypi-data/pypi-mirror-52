import json
from urllib.parse import quote, urlencode
from base64 import b32encode
from pathlib import Path
import xml.etree.ElementTree as ET

import pyqrcode
from slugify import slugify


class Extractor:
    def __init__(self, finput):
        self._finput = Path(finput)
        if not self._finput.exists():
            raise IOError("'{}' doesn't exist".format(finput))
        self._finput = self._finput.resolve()

    def parse_el(self):
        tree = ET.parse(str(self._finput))
        root = tree.getroot()
        res = {}
        for child in root:
            name = child.attrib.get("name", "tokenOrder")
            data = json.loads(child.text)
            if name != "tokenOrder":
                secret = bytes((x + 256) & 255 for x in data.get("secret"))
                res[name] = {"secret": b32encode(secret).decode()}
                issuer = data.get("issuerAlt", None)
                issuer = data.get("issuerInt", issuer)
                issuer = data.get("issuerExt", issuer)
                if issuer is not None:
                    res[name]["issuer"] = issuer
                image = data.get("image", None)
                if image is not None:
                    res[name]["image"] = image
        return res

    def run(self, output=None):
        res = self.parse_el()
        if output is None:
            for k, v in res.items():
                print("{}: {}".format(k, v["secret"]))
        else:
            Path(output).write_text(json.dumps(res))

    def qrcode(self, kind="term", output=None):
        data = json.loads(self._finput.read_text())
        if output is None:
            output = self._finput.parent
        else:
            output = Path(output).resolve()
        for label, query in data.items():
            p = str(output / slugify(label))
            uri = "otpauth://totp/{}?{}".format(quote(label), urlencode(query))
            qr = pyqrcode.create(uri)
            if kind == "term":
                print(label)
                print(qr.terminal(quiet_zone=1))
                input("wait for the next one...")
            elif kind == "svg":
                qr.svg(p + ".svg", scale=8)
            elif kind == "eps":
                qr.eps(p + ".eps", scale=8)
            else:
                raise ValueError(
                    "'kind' must be one of these values ('term', 'svg', 'eps')"
                )
