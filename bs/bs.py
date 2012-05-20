import string
import sys
from bs4 import BeautifulSoup
import chardet
import codecs



def get_title(soup):
    return 

def read_html(filename):
    fr=open(filename)
    doc=''.join(fr.readlines())
    fr.close()
    _code=""
    scode=doc.find("charset=")
    if scode!=-1:
        ecode=doc.find("\"",scode)
        _code=doc[scode+8:ecode]
        doc=unicode(doc,_code,'ignore')
    soup=BeautifulSoup()
    if _code!="":
        soup=BeautifulSoup(doc)
    else:
        soup=BeautifulSoup(doc,from_encoding=chardet.detect(doc)['encoding'])
    #print soup.original_encoding


    title=unicode(soup.title.string).encode("utf8","ignore").rstrip().strip()
    doc=soup.descendants
    find=0
    parent=""
    for tag in doc:
        if len(unicode(tag).encode("utf8","ignore"))==0:
            continue
        midu = float(len(unicode(tag.string).encode("utf8","ignore")))/len(unicode(tag).encode("utf8","ignore"))
        if str(type(tag))=="<class 'bs4.element.NavigableString'>":
            tag_text=unicode(tag).encode("utf8","ignore").rstrip().strip()
            if title.find(tag_text)==0 and len(tag_text)>1 and tag_text!=title:
                find=1
                continue
        if find==1:
            if midu >= 0.5 and len(unicode(tag).encode("utf8","ignore"))>1:
                if str(type(tag)).find("NavigableString")!=-1:
                    print unicode(tag).encode("utf8","ignore").rstrip().strip()
                    break
                for child in tag.descendants:
                    print unicode(child).encode("utf8","ignore").rstrip().strip()
                break
            

read_html(sys.argv[1])
