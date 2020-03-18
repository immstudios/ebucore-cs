#!/usr/bin/env python3

import os
import sys
import json

from nxtools import *


src_dir = "cs"
lang_attr = '{http://www.w3.org/XML/1998/namespace}lang'


def crawl_terms(root, indent=2):
    for term in root.findall("Term"):
        value = term.attrib["termID"]

        try:
            if term.find("ValidityFlag").text != "1":
                logging.debug("skipping invalidated term id", value)
                continue
        except:
            pass

        settings = {"aliases" : {}}

        for name in term.findall("Name"):
            try:
                lang = name.attrib[lang_attr]
            except:
                logging.error(term.text, name.text)
                continue
            alias = name.text
            settings["aliases"][lang] = alias

        yield value

        for row in crawl_terms(term, indent=indent+2):
            yield row


for csfile in get_files(src_dir, exts=["xml"]):
    logging.info("Parsing", csfile.base_name)
    x = xml(csfile.open().read())
    csname = x.attrib["uri"]
    try:
        tname = csfile.base_name.split("_")[1].replace("CS", "", -1)
    except:
        continue

    used_values = []
    for value in crawl_terms(x):
        if value in used_values:
            logging.error("{} already present in this scheme".format(value))
            continue
        used_values.append(value)
        pass
