from datetime import datetime
import tornado.web
#import tornado.ioloop
from data.enum import CSts,CEvt
from general.utility.logger import log
from processor import GrProcess

class CJsonHandler(tornado.web.RequestHandler):

    import process.MatrixJsonPostHandler as PostJ

    #"""
    def get(self):
        try:
            log.debug("main Call get!!! {0}".format( datetime.now().time()))
            GrProcess.MatrixGetHandler(self)
            self.CustomWrite()
        except Exception as e:
            print(e)
        finally:
            log.debug("main Call Gend!!! {0}".format( datetime.now().time()))

    def CustomWrite(self,len_body='0',header="header.html"):
        _list=GrProcess.GetList()
        _message=GrProcess.GetMessage()
        import general.template.CustomTemplateWriter as _Writer
        #self.set_header("Content-type", "application/json")
        _Writer.write(self,"",_list,_message,"","",len_body,header)

    async def post(self):
        len_body=0
        try:
            log.info("main Json Call post!!! {0}".format( datetime.now().time()))
            len_body=self.PostJ.MatrixJsonPostHandler(self,GrProcess)
            self.CustomWrite(len_body,"result.html")

        except Exception as e:
            print(e)
            pass
        finally:
            log.info("main json Call Pend!!! {0}".format( datetime.now().time()))
