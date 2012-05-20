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
    ex_html=ExtractHtml(html_doc)
    res_dict=ex_html.GetResultDict()

def output():
    print res_dict["extract_successful"]
    print res_dict["real_title"]

read_html_doc()
run()
output()
