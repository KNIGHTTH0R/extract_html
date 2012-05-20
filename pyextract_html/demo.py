import sys
import string
import urllib
import pyextract_html


_extractor=pyextract_html.pyextract_html()

def run():
    while 1:
        url=sys.stdin.readline()
        if not url:
            break
        url=url.rstrip()
        html=""
        try:
            page=urllib.urlopen(url)
            html=page.read()
            page.close()
        except:
            continue
        if html!="":
            _extractor.pre_process(html)
            print _extractor.get_title()
        
run()
