#import os
from os import path
from datetime import datetime
import tornado.web
import tornado.ioloop
from general.utility.logger import log
from processor import GrProcess  #CProcess,
from process.JsonHandler import CJsonHandler

class MainHandler(tornado.web.RequestHandler):

    async def get(self):
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
        _imgfile=GrProcess.GetImg()
        _Emsg=GrProcess.GetMessage2()
        import general.template.CustomTemplateWriter as _Writer
        #self.set_header("Content-type", "text/html")
        _Writer.write(self,_imgfile,_list,_message,_Emsg[0],_Emsg[1],len_body,header)

    async def post(self):
        import process.MatrixPostHandler as Posth
        try:
            log.debug("main Call post!!! {0}".format( datetime.now().time()))
            len_body=Posth.MatrixPostHandler(self,GrProcess)
            """
            if( len_body < 0 ):
                # 返却ﾚサイズがマイナス時は終了要求とする
                tornado.ioloop.IOLoop.current().stop()
            """
            self.CustomWrite(len_body,"result.html")

        except Exception as e:
            print(f"{type(e)} {e}")
        finally:
            log.debug("main Call Pend!!! {0}".format( datetime.now().time()))

BASE_DIR = path.dirname(__file__)

application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/wd/hub/",CJsonHandler),  # for Json
        ],
        template_path=path.join(BASE_DIR, 'templates'),
        static_path=path.join(BASE_DIR, 'static'),
)

#
# Pythonの例外処理（try, except, else, finally）
# https://note.nkmk.me/python-try-except-else-finally/
#

if __name__ == '__main__':
    """
    import sys

    if "debugpy" in sys.modules:
        print('VSCodeからデバッグされてます')
    else:
        print('VSCodeからデバッグされてません')
    """

    application.listen(8888)
    GrProcess.open()
    try:
        log.error(f'loop start!!!!')
        tornado.ioloop.IOLoop.current().start()
        log.error(f'{__name__} stop success')
    except Exception as e:
        log.error(f'Error ::app.py Main [e]')
    finally:
        GrProcess.close()
        pass