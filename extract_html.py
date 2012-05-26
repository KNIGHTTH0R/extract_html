import string
import sys
from bs4 import BeautifulSoup,Comment,NavigableString

__DEBUG_OUTPUT__=False
HTML_STOP_TAG={"textarea":1,"iframe":1,"script":1,"input":1,"style":1}
HTML_CONTENT_TAG={"div":1,"article":1}
HTML_COMMENTS_TAG={"li":1,"ul":1,"ol":1,"dl":1}

class ExtractHtml:
    def __init__(self, doc , DEBUG=False):
        global __DEBUG_OUTPUT__
        '''Constructor:'''
        '''@doc : original html document(coding utf8)'''
        '''@return : class itself'''
        __DEBUG_OUTPUT__=DEBUG
        self.__result_dict={"STATE":"False","title":"","content":"","comment":""}
        self.__density=0.5
        self.__coding="utf8"
        self.__parser="html5lib"        
        self.__soup=None
        
        if self.__beautifulsoup(doc):
            self.__run_extractor()

    def __extract_stop_tag(self):
        all_tags=list(self.__soup.descendants)
        for tag in all_tags:
            if isinstance(tag,Comment):
                tag.extract()
            elif isinstance(tag, NavigableString):
                continue
            else:
                if tag.name in HTML_STOP_TAG:
                    tag.extract()

    def __beautifulsoup(self,doc):
        '''using beautifulsoup parser the html doc'''
        try:
            self.__soup=BeautifulSoup(doc, self.__parser, from_encoding=self.__coding)
        except Exception,e:
            if __DEBUG_OUTPUT__:
                print >> sys.stderr,"Error: when __beautifulsoup1 - ",e
            return False
        self.__extract_stop_tag()
        try:
            self.__result_dict["title"]=self.__soup.title.next_element.encode(self.__coding)
            self.__result_dict["content"]=self.__soup.body.encode(self.__coding)
        except Exception,e:
            if __DEBUG_OUTPUT__:
                print >> sys.stderr,"Error: when __beautifulsoup2 - ",e
            #return False
        return True

    def __has_chidren(self,tag):
        try:
            tag.children
            return True
        except:
            return False

    def __is_comment_tag(self,parent):
        if isinstance(parent, NavigableString):
            return False
        if not self.__has_chidren(parent):
            return False
        tag_count=0.0
        cm_count=0.0
        for child in parent.children:
            if not isinstance(child, NavigableString):
                if child.name in HTML_COMMENTS_TAG:
                    cm_count+=1.0
            tag_count+=1.0
        if cm_count/tag_count>=self.__density:
            return True
        return False

    def __recursion_get_most_important_child_block(self, parent):
        content_tag=parent
        if not self.__has_chidren(parent):
            return content_tag
        parent_len=float(len(parent.get_text()))
        if parent_len<=0:
            return content_tag
        imp_len=0.0
        imp_tag=None
        comments_len=0.0
        comment_tag=None
        for child in parent.children:
            child_len=0.0
            if isinstance(child, NavigableString):
                continue
            if child.name in HTML_COMMENTS_TAG:
                continue
            elif child.name in HTML_CONTENT_TAG:
                child_len=float(len(child.get_text()))
            if child_len>imp_len:
                if self.__is_comment_tag(child):
                    if child_len>comments_len:
                        comment_tag=child
                        child_len=comments_len
                    continue
                imp_len=child_len
                imp_tag=child
        if imp_len/parent_len>=self.__density:
            return self.__recursion_get_most_important_child_block(imp_tag)
        return (content_tag, comment_tag)

    def __run_extractor(self):
        (content_tag, comment_tag)=(None,None)
        try:
            (content_tag, comment_tag)=self.__recursion_get_most_important_child_block(self.__soup.body)
        except Exception,e:
            if __DEBUG_OUTPUT__:
                print >> sys.stderr,"Error: when __recursion_get_most_important_child_block - ",e
            return
        if content_tag!=self.__soup.body:
            self.__result_dict["STATE"]="True"
            if comment_tag!=None:
                self.__result_dict["comment"]=unicode(comment_tag).encode(self.__coding,"ignore")
                comment_tag.extract()
            self.__result_dict["content"]=unicode(content_tag).encode(self.__coding,"ignore")
        
    def GetResultDict(self):
        return self.__result_dict


    

