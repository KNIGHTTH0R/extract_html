#coding:gbk
import string
import chardet
import re

class pyextract_html:
    def __init__(self):
        self._html=""
        self._title=""
        self._content=""
        self._code=""
        
    '''preprocessing'''
    def pre_process(self, html):
        self._html=html
        self._code="utf8"
        return self._html


    def get_title(self):
        tstart=self._html.find("<title>")
        tend=self._html.find("</title>")
        self._title = self._html[tstart+7:tend].rstrip().strip()
        re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA
        re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
        re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
        #re_br=re.compile('<br\s*?/?>')#处理换行
        #re_h=re.compile('</?\w+[^>]*>')#HTML标签
        re_comment=re.compile('<!--[^>]*-->')#HTML注释
        s=re_cdata.sub('',self._html)#去掉CDATA
        s=re_script.sub('',s) #去掉SCRIPT
        s=re_style.sub('',s)#去掉style
        #s=re_br.sub('\n',s)#将br转换为换行
        #s=re_h.sub('\n',s) #去掉HTML标签
        s=re_comment.sub('',s)#去掉HTML注释
        #去掉多余的空行
        #blank_line=re.compile('\n+')
        #s=blank_line.sub('\n',s)
        #s=s.replace("&nbsp;","")
        lines=s.split("\n")
        max_len=len(self._title)
        i=0
        for line in lines:
            line=line.strip().rstrip()
            #print line
            if self._title.find(line)==0 and len(line)>1:
                if len(line)<max_len:
                    print line
            i+=1
        return self._title

    def get_content(self):
        print self._html

