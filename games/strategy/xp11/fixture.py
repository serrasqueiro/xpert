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
    # Table shorts
    print("# :: tables:", fixt["tables"])
    return ""

def dump_anchors(fixt):
    for key in sorted(fixt["a-index"]):
        entry = fixt["a-index"][key]
        astr = entry["string"]
        id_kind = entry["@id"]
        if id_kind is None:
            continue
        an_id = entry["attrs"].get("id")
        s_id = "" if an_id is None else f", {an_id}"
        check = f'"{astr}": {entry["href"]}{s_id}'
        print(f"::: a-index {key} {id_kind}:", check)
        if id_kind and id_kind.endswith("hplResultat"):
            print()
    return True

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
    all_a, t_index = {}, {}
    tabular = [
        {
            "index": idx+1,
            "table-id": table.attrs.get("id"),
            "table": table,
        } for idx, table in enumerate(soup.find_all("table"))
    ]
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
    # t_index is a dictionary with table indexes and then the table content,
    #	[(this["index"], this["table-id"]) for this in tabular if this["table-id"] is not None]
    for this in tabular:
        tab_id = this["table-id"]
        if tab_id is None:
            continue
        t_index[this["index"]] = {
            "table-id": tab_id,
            "table": this["table"],
            "table-rows": iterate_over([row for row in this["table"].children]),
        }
    # Combining own properties
    obj = {
        "soup": [soup],
        "title": soup.title.string.strip(),
        "anchors": anchors,
        "a-index": all_a,
        "tables": tabular,
        "t-index": t_index,
    }
    res = {
        "fixture": obj,
    }
    print("::", "title:", obj["title"])
    return res

def iterate_over(alist:list) -> list:
    """ Returns the list of rows. """
    res = []
    for row in alist:
        if row.name not in ("tr",):
            continue
        elem = {
            "attrs": row.attrs,
            "row": [elem for elem in row.children if elem.name == "td"],
        }
        res.append(elem)
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
