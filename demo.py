from extract_html import ExtractHtml

res_dict={}

def read_html_doc():
    fr=open("demo.html")
    html_doc="".join(fr.readlines())
    fr.close()
    return html_doc

def run():
    global res_dict
    html_doc=read_html_doc()
    DEBUG=True
    ex_html=ExtractHtml(html_doc, DEBUG)    #using ExtractHtml Lib with two parameters:
                                            #'html_doc' -  The coding must be utf8
                                            #'DEBUG'    -  It's not nessary, the default value is False, when it is True,
                                            #              the lib would output exception information to sys.stderr
    res_dict=ex_html.GetResultDict()        #get result, the result is dict type, four keys in it:
                                            #   keys :
                                            #        1. 'STATE'   - Is exctracting successful or not
                                            #                       'True' means extracting successful
                                            #                       'False' means extracting failure, would give the 'body' to 'content'
                                            #        2. 'title'   - Html title
                                            #                       Now it just return the string in title tag
                                            #                       Try it best to return some strings, but sometimes would return empty
                                            #        3. 'content' - Html content
                                            #                       Not very good for image type html, it's very good for text type html
                                            #                       Coding with utf8
                                            #                       Try it best to return some strings, but sometimes would return empty
                                            #        4. 'comment' - Try to get comments.

def output():
    print res_dict["STATE"]
    #print unicode(res_dict["title"])
    fw=open("content.html","w")
    fw.write("<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\">")
    fw.write(res_dict["content"])
    fw.close()
    fw=open("comments.html","w")
    fw.write("<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\">")
    fw.write(res_dict["comment"])
    fw.close()

read_html_doc()
run()
output()
