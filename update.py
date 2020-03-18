#!/usr/bin/env python3

import os
import io
import re
import sys

try:
    import requests
except ImportError:
    print("Error: python-requests module is required")
    sys.exit(-1)

ROOT_URL = "http://www.ebu.ch/metadata/cs/"
CS_DIR = "original/"

def cs_list():
    index = requests.get(ROOT_URL)
    urls = re.findall(r'href=[\'"]?([^\'" >]+)', index.text)
    for url in urls:
        if not url.endswith(".xml"):
            continue
        yield url

if __name__ == "__main__":
    for fname in cs_list():
        output_path = os.path.join(CS_DIR, fname)
        url = ROOT_URL + fname
        print ("Downloading {}".format(fname))
        sheet = requests.get(url)
        if sheet.status_code != 200:
            print ("Error {} occured during requesting {}".format(sheet.response_code, fname))
            continue
        with io.open(output_path, "w", encoding="utf8") as f:
            f.write(sheet.text)
