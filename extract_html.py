''''''
''''''
import string
from bs4 import BeautifulSoup

BS4TAG_NavigableString="<class 'bs4.element.NavigableString'>"

class ExtractHtml:
    def __init__(self, doc, extractor_name="density"):
        '''Constructor:'''
        '''@doc : original html document'''
        '''@extractor_name : assign the extract method, default is density method'''
        '''@return : class itself'''
        self.__result_dict={"extract_successful":"False","ori_title":"","real_title":"", \
                            "content":"","ori_html":"","prettify_html":""}
        self.__title_tag_index=0
        self.__titleTag=None
        self.__density=0.5
        self.__coding="utf8"
        self.__middle_coding="utf8"
        self.__parser="html5lib"        
        self.__soup=None

        self.__result_dict["ori_html"]=doc
        if self.__beautifulsoup():
            if self.__run_extractor(extractor_name):
                self.__result_dict["extract_successful"]="True"

    def __beautifulsoup(self):
        '''using beautifulsoup parser the html doc'''
        try:
            self.__soup=BeautifulSoup(self.__result_dict["ori_html"],self.__parser, \
                                  from_encoding=self.__coding)
            #self.__result_dict["prettify_html"]=self.__soup.prettify(self.__coding)
            self.__titleTag=self.__soup.title.next_element
            self.__result_dict["ori_title"]=unicode(self.__titleTag).encode(self.__coding,"ignore")
        except:
            return False
        return True
        
    def __extractor_real_title_by_prefix_match(self):
        global BS4TAG_NavigableString
        #find title tag in html tree
        for tag in self.__soup.descendants:
            self.__title_tag_index+=1
            if tag==self.__titleTag:
                break
        #find real title
        tags=list(self.__soup.descendants)
        lens=len(tags)
        max_len=0
        index=self.__title_tag_index
        while index<lens:                                          #traversal all tags
            if str(type(tags[index]))==BS4TAG_NavigableString:     #tag is BS4TAG_NavigableString
                if self.__titleTag.find(tags[index])!=-1:             #tag is the prefix of ori_title
                    if len(tags[index])>max_len and len(tags[index])!=len(self.__titleTag): #condition
                        max_len=len(tags[index])
                        self.__result_dict["real_title"]=tags[index]
                        self.__title_tag_index=index
            index+=1
        if self.__result_dict["real_title"]!="":
            return True
        else:
            return False

    def __extractor_self_content_by_density(self,tag):
        content=""
        if len(unicode(tag).encode(self.__middle_coding,"ignore").rstrip().strip())==0:
            return content
        if str(type(tag))==BS4TAG_NavigableString:
            return content
        density=0.0
        try:
            density=float(len(unicode(tag.get_text()).encode(self.__middle_coding,"ignore")))/len(unicode(tag).encode(self.__middle_coding,"ignore"))
        except:
            pass
        if density>=self.__density:
            content+=unicode(tag).encode(self.__middle_coding,"ignore")
        return content
        
    def __extractor_children_content_by_density(self,tags):
        content=self.__extractor_self_content_by_density(tags)
        if content!="":
            return content
        for tag in tags.children:
            if len(unicode(tag).encode(self.__middle_coding,"ignore").rstrip().strip())==0:
                continue
            if str(type(tag))==BS4TAG_NavigableString:
                continue
            density=0.0
            try:
                density=float(len(unicode(tag.get_text()).encode(self.__middle_coding,"ignore")))/len(unicode(tag).encode(self.__middle_coding,"ignore"))
            except:
                pass
            if density>=self.__density:
                content+=unicode(tag).encode(self.__middle_coding,"ignore")
            else:
                content+=self.__extractor_children_content_by_density(tag)
        return content

    def __extractor_content_by_density(self):
        successful=False
        cur_tag=list(self.__soup.descendants)[self.__title_tag_index].parent
        for next_sibling in cur_tag.next_siblings:
            if len(unicode(next_sibling).encode(self.__middle_coding,"ignore").rstrip().strip())==0:
                continue
            if str(type(next_sibling))==BS4TAG_NavigableString:
                continue
            self.__result_dict["content"]+=self.__extractor_children_content_by_density(next_sibling)
            successful=True
        return successful

    def __extract_by_density(self):
        '''densityc extractor'''
        successful=False
        if self.__extractor_real_title_by_prefix_match(): #firstly, extract real title 
            if self.__extractor_content_by_density():     #secondly, extract content by density
                successful=True
        return successful

    def __run_extractor(self,extractor_name):
        '''invoke different extractors by extractor_name'''
        successful=False
        if extractor_name=="density":
            successful=self.__extract_by_density()
        self.__extract_successful=successful
        return successful

    def GetResultDict(self):
        return self.__result_dict
        














    

    
    
