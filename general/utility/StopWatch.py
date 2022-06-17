import datetime
from general.utility.logger import MatrixFunction,log

def MatrixFunctionEx(func):
#def StopWatch(func):
    def wrapperM(Prams,Sts,Evt):
        def gets( s ):
            t=f"{s/3600:.0f}h:{s/60:.0f}m:{s%60}s"
            return(t)
        
        # 処理開始直前の時間
        start= datetime.datetime.now()

        # 処理実行
        try:
            inner_func=MatrixFunction(func)
            result=inner_func(Prams,Sts,Evt)
        finally:
            # 処理終了直後の時間から処理時間を算出
            _end=datetime.datetime.now()
            elapsed_time = _end - start

            # 処理時間を出力
            #log.info( f"{func.__name__} finish!! { gets(elapsed_time.seconds)}")
            log.critical( f"{func.__name__} finish!! { gets(elapsed_time.seconds)} {_end.strftime('%H:%M:%S')}")  #now.strftime('%Y/%m/%d %H:%M:%S')
        return result
    return wrapperM

def StopWatchEx(ownerName):
#def TradeSummarySetTradeResult(ownerName):
    def inner_funcTradeS1(func):
        def inner_funcTradeS2(*args,**kwargs):
            def gets( s ):
                t=f"{s/3600:.0f}h:{s/60:.0f}m:{s%60}s"
                return(t)
            # 処理開始直前の時間
            start= datetime.datetime.now()
            try:
                result = func(*args,**kwargs)
            finally:
                # 処理終了直後の時間から処理時間を算出
                _end=datetime.datetime.now()
                elapsed_time = _end - start
                # 処理時間を出力
                log.critical( f"{ownerName} finish!! { gets(elapsed_time.seconds)} {_end.strftime('%H:%M:%S')}")  #now.strftime('%Y/%m/%d %H:%M:%S')
            return result
        return inner_funcTradeS2
    return inner_funcTradeS1

def StopWatch(func):
    def wrapperS(*args, **kargs):
        def gets( s ):
            #return( a/3600,a//60 )
            #t=f" base={a} h:{a/3600:.0f}:{a/60:.0f}:{a%60}{type(a)}"
            t=f"{s/3600:.0f}h:{s/60:.0f}m:{s%60}s"
            return(t)

        # 処理開始直前の時間
        start= datetime.datetime.now()
        #start = datetime.datetime(2022, 4, 28, 23, 59, 59, 0000)

        # 処理実行
        try:
            result = func(*args, **kargs)
        finally:
            # 処理終了直後の時間から処理時間を算出
            elapsed_time = datetime.datetime.now() - start
            #aft_days = start + timedelta(weeks=0,days=1,hours=1,minutes=0,seconds=1,milliseconds=0,microseconds=0)
            #aft_days = datetime.datetime(2022, 4, 29, 0, 0, 0, 0000)
        
            # 処理時間を出力
            print( f"{func.__name__} finish!! { gets(elapsed_time.seconds)}")
            #print( f"{func.__name__} finish!! { gets(elapsed_time.seconds)}")
        
        return result
    return wrapperS

