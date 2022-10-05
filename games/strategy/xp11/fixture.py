# (c)2022  Henrique Moreira

""" fixture.py - first attempt to read from xperteleven www!
"""

# pylint: disable=missing-function-docstring

import sys
import requests

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
    return ""

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

if __name__ == "__main__":
    main()
