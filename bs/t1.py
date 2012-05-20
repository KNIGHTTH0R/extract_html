import string
import sys
from bs4 import BeautifulSoup
import chardet
import codecs


def find_real_title(title,soup):
    num=0
    for tag in soup.descendants:
        num+=1
        if tag==title:
            break
    tags=list(soup.descendants)
    lens=len(tags)
    max_len=0
    index=-1
    real_title=""
    i=num
    while i<lens:
        #if str(type(tags[i])).find("Tag")!=-1:
        #    if tags[i].name=="h2":
        #        print unicode(tags[i]).encode("gbk")
        if str(type(tags[i]))=="<class 'bs4.element.NavigableString'>":
            if title.find(tags[i])!=-1:
                if len(tags[i])>max_len and len(tags[i])!=len(title):
                    max_len=len(tags[i])
                    real_title=tags[i]
                    index=i
        i+=1
    return (index,real_title)

def get_self_content(tag):
    content=""
    if len(unicode(tag).encode("utf8","ignore").rstrip().strip())==0:
        return content
    if str(type(tag))=="<class 'bs4.element.NavigableString'>":
        return content
    density=float(len(unicode(tag.get_text()).encode("utf8","ignore")))/len(unicode(tag).encode("utf8","ignore"))
    if density>=0.0:
        content+=unicode(tag).encode("utf8","ignore")
    return content
    
def get_children_content(tags):
    content=get_self_content(tags)
    if content!="":
        return content
    for tag in tags.children:
        if len(unicode(tag).encode("utf8","ignore").rstrip().strip())==0:
            continue
        if str(type(tag))=="<class 'bs4.element.NavigableString'>":
            continue
        density=float(len(unicode(tag.get_text()).encode("utf8","ignore")))/len(unicode(tag).encode("utf8","ignore"))
        if density>=0.0:
            content+=unicode(tag).encode("utf8","ignore")
        else:
            content+=get_children_content(tag)
    return content

def get_content(index,soup):
    content=""
    cur_tag=list(soup.descendants)[index].parent
    for next_sibling in cur_tag.next_siblings:
        if len(unicode(next_sibling).encode("utf8","ignore").rstrip().strip())==0:
            continue
        if str(type(next_sibling))=="<class 'bs4.element.NavigableString'>":
            continue
        content+=get_children_content(next_sibling)
    return content
    
def test(f1):
    fr=open(f1)
    doc=fr.readlines()
    fr.close()
    soup=None
    try:
        soup=BeautifulSoup("".join(doc),"html5lib",from_encoding="utf8")
    except:
        print "bs4 error"
        return
    tag_title=soup.title
    title=tag_title.next_element
    (index,real_title)=find_real_title(title,soup)
    print title
    print index,real_title
    #fw=open("ttt.txt",'w')
    #fw.write(soup.prettify("utf8"))
    #fw.close()
    if index!=-1:
        content=get_content(index,soup)
        fw=open("test.html",'w')
        fw.write("<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\">")
        fw.write(content)
        fw.close()
        
test(sys.argv[1])
