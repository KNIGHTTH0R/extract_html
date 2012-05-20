import string
import sys
from bs4 import BeautifulSoup
import chardet
import codecs


def test(f1):
    fr=open(f1)
    doc=fr.readlines()
    fr.close()
    soup=BeautifulSoup("".join(doc),from_encoding="utf8")
    tags=soup.children
    for tag in tags:
        if str(tag).rstrip().strip()!="":
            try:
                tag.get_text()
            except:
                continue
            strlen=len(unicode(tag.get_text()).encode("gbk","ignore"))
            lens=len(unicode(tag).encode("gbk","ignore"))
            dis=float(strlen)/lens
            if dis>=0.5:
                print unicode(tag).encode("gbk","ignore")

test(sys.argv[1])
