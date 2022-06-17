from datetime import datetime,time,timedelta
import tornado.ioloop
from data.enum import CEvt,CPpsm
from data.environment.LivingFieldEnv.BrowserEnv import BrEmv
from data.Param import CParam
from general.utility.logger import log
from selenium.common.exceptions import NoSuchElementException
from concurrent.futures import ProcessPoolExecutor
import process.MatrixTable as Matrix

Params=CParam()

# スレッドエラーハンドリング
async def ErrorHandler():
    e=GrProcess.GetLastException()
    #log.error(f"thread Exception {e}")
    log.error(f"スレッドで例外発生 {e}")
    #raise e

class CProcess():

    from general.data.Estimate.visualization import GraphDraw2
    from general.data.informationSystem import CinformationSystem
    info=CinformationSystem()

    #メンバー
    def GetLastException(self):
        return(Params.e) 

    def MatrixBaseHandler(self,evt):
        _ret=self.__MatrixHandler(self,Params,evt)
        #return(_ret)

    def MatrixGetHandler(self,owner):
        Params.Receive=owner
        #Params.Msg="call Get!! 特にないです"
        _ret=self.__MatrixHandler(owner,Params,CEvt.GET)
        return(_ret)

    def MatrixPostHandler(self,owner,evt,body):
        Params.Receive=body
        #Params.Msg="call Post!! 特にないです"
        _ret=self.__MatrixHandler(owner,Params,evt)
        return(_ret)

    def MatrixJsonPostHandler(self,owner,evt,json_data):
        Params.Receive=json_data
        #Params.Msg="call Json Post!! 特にないです"
        _ret=self.__MatrixHandler(owner,Params,evt)
        return(_ret)

    def __MatrixHandler(self,owner,Params,evt):
        _isExit=False
        try:
            _isExit= Matrix.MatrixHandler(owner,Params,evt)
            if( _isExit ):
                tornado.ioloop.IOLoop.current().stop()
        except Exception as e:
            log.error(e)
            tornado.ioloop.IOLoop.current().run_sync(ErrorHandler)
            pass
        return(_isExit)

    def GetList(self):
        #print(type(Params.dfs))
        i=2234.987
        _Array=None
        try:
            _Array=[ self.info.getHtml(Params.dfs,BrEmv.Digits),
                 #Params.dfs.to_html(),
                Params.TradeSummary.getHtml(BrEmv.Digits),
                Params.TradeMsg ]
        except Exception as e:
            log.error(e)
    
        #_Array=["bbbbbb","aaaaa",str(i)]
        #print(type(_Array))
        return(_Array)

    def GetImg(self):
        _img=""
        try:
            if ( type(Params.trade.AannotateList) is list ):
                _img=self.GraphDraw2(Params.trade.table,Params.trade.AannotateList)
        except Exception as e:
            log.error(e)

        return( _img)

    def GetMessage(self):
        return(Params.Msg)

    def GetMessage2(self):
        _args=Params.EstiMsg
        if( type(_args) is not list ):
          return(['',''])
        return(Params.EstiMsg)

    #タイマーモジュールはグローバル属性に勝手になってしまう
    #@FunctionDisplay
    def __OnTimer__(self):
        #log.error("Call CallBack_OnTimer!!!")
        PERIOD = BrEmv.RefreshRate
        ioloop = tornado.ioloop.IOLoop.current()
        if( PERIOD !=0 ):
            __ioloop = tornado.ioloop.IOLoop.current()
            __ioloop.add_timeout(timedelta(seconds=PERIOD), self.__OnTimer__)
            #__ioloop.add_timeout( time().second+PERIOD, self.__OnTimer__)
            #ioloop.add_timeout(datetimr.time + PERIOD, self.__OnTimer_)
            pass
        import process.MatrixJsonPostHandler as PostJ
        PostJ.OnRequest(self,Params )
        self.__MatrixHandler(self,Params,CEvt.TIMER )
        pass

    def __OnPageRefresh__(self):
        def __CalNextInterval(t1,p,c):
            t3=(t1+p if t1 < c else t1) ;
            t2=((p+c- (t1+p if t1 < c else t1) ))
            log.info(f"cycl is { t2 }" )
            return(t2)

        self.__MatrixHandler(self,Params,CEvt.REFRESH )
        #log.error( f"{__name__}: __OnPageRefresh_ run {datetime.datetime.now()}") 
        PERIOD = __CalNextInterval( datetime.now().second,\
                            BrEmv.PageRefresh,BrEmv.TriggerSeconds )

        ioloop = tornado.ioloop.IOLoop.current()
        if( BrEmv.PageRefresh !=0 ):
            __ioloop = tornado.ioloop.IOLoop.current()
            __ioloop.add_timeout(timedelta(seconds=PERIOD), self.__OnPageRefresh__)
            #__ioloop = tornado.ioloop.IOLoop.current(),self.__OnPageRefresh__)
            #__ioloop.add_timeout(timedelta(seconds=PERIOD), 
            #__ioloop.add_timeout(self.__OnPageRefresh__)timedelta(seconds=PERIOD),self.__OnPageRefresh__)
            #__ioloop.add_timeout(time().second + PERIOD, self.__OnPageRefresh__)

    def __CallBack_OnInit__( self,Params ) :
        log.error("Call CallBack_OnInit!!!")
        self.__MatrixHandler(self,Params,CEvt.BOPEN )
        self.__OnTimer__()
        self.__OnPageRefresh__()
        pass

    # 0)ブロッキング (処理が終わるまで他のリクエストを受け付けない)
    def __Single_CallBack__( self,owner,MyParams,evt ) :
        self.__MatrixHandler(owner,MyParams,evt )

    # 1) マルチスレッド (1つのCPUで並行処理))
    async def __Thread_CallBack__( self,owner,MyParams,evt ) :
        #log.error("Call __Thread_CallBack__!!!")
        ioloop = tornado.ioloop.IOLoop.current()
        await ioloop.run_in_executor( None,
                                     self.__MatrixHandler,owner,MyParams,evt )

    # 2) マルチプロセス (複数のCPUで並列処理)
    # pickle化できないパラメータは渡せないので用途は限定される
    #@classmethod
    async def __Process_CallBack__( self,owner,MyParams,evt ) :
        #log.error("Call __Process_CallBack__!!!")
        ioloop = tornado.ioloop.IOLoop.current()
        await ioloop.run_in_executor( ProcessPoolExecutor(),
                                        self.MatrixBaseHandler,CEvt.CON_FIN )
        from data.enum import CSts
        MyParams.sts( CSts.LOGIN)

    def __Set_CallBack(self,evt,MyParams,func ):
        ioloop = tornado.ioloop.IOLoop.current()
        ioloop.add_callback( func,self,MyParams,evt )
        pass

    def SetCallBack( self,evt,mode=CPpsm.SINGLE ) :
        if( mode ==CPpsm.THREAD ):
            self.__Set_CallBack(evt,Params,self.__Thread_CallBack__)

        elif(mode == CPpsm.PROCESS ):
            self.__Set_CallBack(evt,Params,self.__Process_CallBack__)
            pass
        else:       # CPpsm.SINGLE
            self.__Set_CallBack(evt,Params,self.__Single_CallBack__)
            pass

    def open(self):
        self.__MatrixHandler(self,Params,CEvt.OPEN )
        ioloop = tornado.ioloop.IOLoop.current()
        ioloop.add_callback(self.__CallBack_OnInit__,Params)
        log.info(f"起動時 {Params.sts()}")
        pass

    def close(self):
        #もうループが終了してるんだからマトリクス処理呼べないじゃん
        #self.__MatrixHandler(self,Params,CEvt.CLOSE )
        from process.matrix.OnClose import OnClose
        OnClose(Params,Params.sts(),CEvt.CLOSE )
        tornado.ioloop.IOLoop.current().stop()
        pass

GrProcess=CProcess()