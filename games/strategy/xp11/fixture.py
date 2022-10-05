# (c)2022  Henrique Moreira

""" fixture.py - first attempt to read from xperteleven www!
"""

# pylint: disable=missing-function-docstring

import sys
import requests
from bs4 import BeautifulSoup


ENCODING = "ISO-8859-1"	# ...or "ascii"
CACHE_FILE = ".xpert.data"
GET_TIMEOUT = 30	# 30 seconds


def main():
    msg = dump_test(sys.argv[1:], CACHE_FILE)
    assert not msg, msg

def dump_test(paths:list, cache_file):
    msg = ""
    assert not paths
    datas = {
        "conf": {
            "timeout": GET_TIMEOUT,
        },
    }
    try:
        with open(cache_file, "rb") as fdin:
            cont = fdin.read()
    except FileNotFoundError:
        cont = None
    if cont is None:
        print("Getting fixtures...")
        msg, data = get_fixture(datas)
    else:
        data = cont
    if msg:
        print("get_fixture():", msg)
        return msg
    if cont is None:
        with open(cache_file, "wb") as fdout:
            fdout.write(data)
    print(f"Cached fixture ({cache_file}):", len(data))
    adict = processor(data)
    fixt = adict["fixture"]
    # Dump anchors
    dump_anchors(fixt)
    return ""

def dump_anchors(fixt):
    for key in sorted(fixt["a-index"]):
        entry = fixt["a-index"][key]
        astr = entry["string"]
        id_kind = entry["@id"]
        an_id = entry["attrs"].get("id")
        s_id = "" if an_id is None else f", {an_id}"
        check = f'"{astr}": {entry["href"]}{s_id}'
        print(f"::: a-index {key} {id_kind}:", check)

def get_fixture(datas:dict) -> tuple:
    myparam = {}
    myurl = "https://xperteleven.com/fixture.aspx?Lid=411258&Lnr=1&dh=2&plang=EN"
    timeout = datas["conf"]["timeout"]
    req = requests.get(url=myurl, params=myparam, timeout=timeout)
    if req.is_redirect:
        return "Unexpected redirect", None
    # req.apparent_encoding is usually utf-8
    if req.encoding != "utf-8":
        return f"Unexpected encoding '{req.encoding}': should be utf-8", None
    text = req.content.decode("utf-8").replace("\r", "")
    cont = text.encode("utf-8")
    return "", cont

def processor(data) -> dict:
    assert isinstance(data, bytes)
    html_doc = data
    soup = BeautifulSoup(html_doc, "html.parser")
    anchors = soup.find_all("a")
    all_a = {}
    for idx, anchor in enumerate(anchors, 1):
        id_kind = None
        an_id = anchor.attrs.get("id")
        if an_id is not None:
            if "Fixture_ctl" in an_id:
                id_kind = an_id.split("Fixture_ctl", maxsplit=1)[-1]
        all_a[idx] = {
            "attrs": anchor.attrs,
            "string": anchor.string,
            "href": handle_href(anchor.attrs.get("href")),
            "@id": id_kind,
        }
    obj = {
        "soup": [soup],
        "title": soup.title.string.strip(),
        "anchors": anchors,
        "a-index": all_a,
    }
    res = {
        "fixture": obj,
    }
    print("::", "title:", obj["title"])
    return res

def handle_href(astr) -> str:
    """ Rework URL http reference """
    if astr is None:
        return ""
    if astr.startswith(("http://", "https://")):
        new = astr.split("://", maxsplit=1)[-1]
    elif astr.startswith("javascript:"):
        new = "-"
    else:
        new = astr
    return new

if __name__ == "__main__":
    main()
