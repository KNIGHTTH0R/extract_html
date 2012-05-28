import string
import sys
from bs4 import BeautifulSoup,Comment,NavigableString

__DEBUG_OUTPUT__=False
HTML_STOP_TAG={"textarea":1,"iframe":1,"script":1,"input":1,"style":1}
HTML_NORMAL_TAG={"center":1}
HTML_CONTENT_TAG={"div":1,"article":1}
HTML_COMMENTS_PARENT_TAG={"ul":1,"ol":1,"dl":1}
HTML_COMMENTS_CHILD_TAG={"li":1,"dt":1,"dt":1}
HTML_DIV_COMMENTS_TAG_STR="div"
HTML_P_TAG_STR="p"
HTML_USER_TYPE_TAG_PREFIX="data-"

class ExtractHtml:
    def __init__(self, doc , DEBUG=False):
        global __DEBUG_OUTPUT__
        '''Constructor:'''
        '''@doc : original html document(coding utf8)'''
        '''@return : class itself'''
        __DEBUG_OUTPUT__=DEBUG
        self.__result_dict={"STATE":"False","title":"","content":"","comment":""}
        self.__density=0.5
        self.__comments_density=0.8
        self.__coding="utf8"
        self.__parser="html5lib"        
        self.__soup=None
        
        if self.__beautifulsoup(doc):
            fw=open("1.txt","w")
            fw.write(self.__soup.prettify("utf8"))
            fw.close()
            self.__run_extractor()

    def __is_empty_tag(self,tag,special_name=""):
        if isinstance(tag,NavigableString):
            if len(tag.rstrip().strip())==0:
                return True
            else:
                return False
        state=False
        if self.__has_children(tag):
            if len(tag.contents)==0:
                state=True
            if len(tag.contents)==1:
                if isinstance(tag.contents[0],NavigableString):
                    if len(tag.contents[0].rstrip().strip())==0:
                        state=True
        if special_name!="":
            if tag.name!=special_name:
                state=False
        return state

    def __head_tail_normalization(self,content_tag):
        if self.__has_children(content_tag):
            children=content_tag.contents
            lens=len(children)
            extract_candidates=[]
            if lens>0:
                for i in range(0,lens):
                    if self.__is_empty_tag(children[i],HTML_P_TAG_STR):
                        extract_candidates.append(children[i])
                    else:
                        break
                i=lens-1
                while i>=0:
                    if self.__is_empty_tag(children[i],HTML_P_TAG_STR):
                        extract_candidates.append(children[i])
                    else:
                        break
                    i-=1
                for tag in extract_candidates:
                    tag.extract()
                        
    def __extract_stop_tag(self):
        all_tags=list(self.__soup.descendants)
        parent_list=[]
        for tag in all_tags:
            if isinstance(tag,Comment):
                parent_list.append(tag.parent)
                tag.extract()
            elif isinstance(tag, NavigableString):
                continue
            else:
                if tag.name in HTML_STOP_TAG:
                    parent_list.append(tag.parent)
                    tag.extract()
        for parent in parent_list:
            if parent==None:
                continue
            if self.__is_empty_tag(parent):
                parent.extract()

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
            self.__result_dict["title"]=str(self.__soup.title.next_element.encode(self.__coding)).rstrip().strip()
            self.__result_dict["content"]=self.__soup.body.encode(self.__coding)
        except Exception,e:
            if __DEBUG_OUTPUT__:
                print >> sys.stderr,"Error: when __beautifulsoup2 - ",e
            #return False
        return True

    def __has_children(self,tag):
        try:
            tag.children
            return True
        except:
            return False

    def __attrs_is_equal(self,attrs1,attrs2):
        if len(attrs1)!=len(attrs2):
            return False
        _equal=True
        for key in attrs1:
            if key not in attrs2:
                return False
            if not key.startswith(HTML_USER_TYPE_TAG_PREFIX):
                if attrs1[key]!=attrs2[key]:
                    return False
        return True

    def __is_comment_tag(self,parent):
        if isinstance(parent, NavigableString):
            return False
        if not self.__has_children(parent):
            return False
        if parent.name in HTML_COMMENTS_PARENT_TAG:
            return True
        tag_count=0.0
        list_count=0.0
        div_cm_count=0.0
        div_cm_attrs=None
        for child in parent.children:
            if not isinstance(child, NavigableString):
                if child.name==HTML_DIV_COMMENTS_TAG_STR:
                    if div_cm_attrs==None:
                        div_cm_attrs=child.attrs
                    elif self.__attrs_is_equal(div_cm_attrs,child.attrs):
                        div_cm_count+=1.0
                elif child.name in HTML_COMMENTS_PARENT_TAG:
                    list_count+=1.0
            tag_count+=1.0
        if (list_count/tag_count)>=self.__density:
            return True
        if (div_cm_count/tag_count)>=self.__comments_density:
            return True
        return False

    def __recursion_get_most_important_child_block(self, parent):
        content_tag=parent
        if not self.__has_children(parent):
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
            if child.name in HTML_COMMENTS_CHILD_TAG:#skip, just handle upper floor
                continue
            elif child.name in HTML_CONTENT_TAG or child.name in HTML_NORMAL_TAG:
                child_len=float(len(unicode(child.get_text().replace(" ","")).encode("gbk","ignore")))
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
            self.__head_tail_normalization(content_tag)
            self.__result_dict["content"]=unicode(content_tag).encode(self.__coding,"ignore")
        
    def GetResultDict(self):
        return self.__result_dict


    

