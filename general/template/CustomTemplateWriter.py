#
# 参考資料
# https://sites.google.com/site/tornadowebja/documentation/core-web-framework/tornado-template
#
from datetime import datetime
import socket
import tornado.template
from data.environment.LivingFieldEnv.BrowserEnv import BrEmv

#def write(self,list,message=''):
def write(self,imgfile,inplist,message='',EstiMsg='',EstiMsg2='',len_body='0',header="header.html",footerMessage='' ):
    loader = tornado.template.Loader("templates")
    #self.set_header("Content-type", "application/json")
    _hostName = socket.gethostname()
    self.write(loader.load(header).generate(static_url=self.static_url,pMessage="",len_body=len_body,hostname=_hostName))
    #text=loader.load("body.html").generate()
    #self.write(text)
    #print(text)
    #print(type(list))

   #f"</tr><tr><td>{BrEmv.visualFile}</td>" +\
    _html= "<!-- TTTT -->"+\
            "<table><tr>"+\
                f'<td\
                <p>last update {datetime.now().replace(microsecond = 0)}</p>\
                <p><img src="{imgfile}"></p>\
                <p>{EstiMsg}</p>\
                <p>{EstiMsg2}</p>\
                <p>{message}</p>\
                <p>{inplist[0]}</p>\
                </td>'\
                f"<td>{inplist[1]}</td>"\
            "</tr></table>" \
            "<!-- TTTT -->"

    #print( _html )
    #self.render( "table.html",item1=list[0],item2="" )
    #print(loader.load("table.html"))
    #self.write(loader.load("table.html").generate(Table1=list[0]))
    self.write(_html)

    if( type(inplist) == list ) and ( len(inplist) > 2 ):
        for i in range(2,len(inplist)):
            #self.write(f"{str(inplist[i])} ")
            self.write(f"{inplist[i]} ")

    self.write(loader.load("footer.html").generate(pMessage=footerMessage))

    """
    #print( loader.templates )
    #self.render("index1.html")
    #self.set_header("Content-type", "text/html")
    self.set_header("Content-type", "application/json")
    #self.render("header.html")
    self.write(Cconfig.dumpsIndent(Param.config))
    #t = template.Template("<html>{{ myvalue }}</html>")
    #print t.generate(myvalue="XXX")
    #loader = template.Loader("/home/btaylor")
    #print loader.load("test.html").generate(myvalue="XXX") 

    ### Python code
    def add(x, y):
        return x + y
        template.execute(add=add)

    ### The template
    {{ add(1, 2) }}
    """
