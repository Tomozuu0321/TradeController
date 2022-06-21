from datetime import datetime
from selenium.common.exceptions import InvalidCookieDomainException

from data.enum import CPmd,CEsti,CFlags #,CBSize
from data.environment.LivingFieldEnv.BrowserEnv import BrEmv
from data.Exceptions import DriverDownException,NotLoginException,ProcessContinuedException
from data.biWconst import const
from data.cookies.CookieHandler import CCookieHandler
import general.utility.bit as Bit
import general.utility.bsize as bs
from general.utility.logger import MatrixFunction,log,getShortName
from general.utility.StopWatch import MatrixFunctionEx
from selenium.common.exceptions import WebDriverException

@MatrixFunctionEx
def BrOpen(Params,sts,evt):

    #オープン処理が動いている場合スキップ
    if(Bit.Chk(Params.Flags,CFlags.B_OPEN)):
        log.error( f" BrOpen Already started ! skip !! {datetime.now()} ") 
        return
    try:
        Params.Flags=Bit.Set(Params.Flags,CFlags.B_OPEN)
        __BrOpen(Params,sts,evt)
    finally:
        Params.Flags=Bit.Clr(Params.Flags,CFlags.B_OPEN)

def __BrOpen(Params,sts,evt):

    _PlatformMode=BrEmv.PlatformMode
    if( _PlatformMode == CPmd.NOSTART ):
        return

    #_driver=Params.driver
    if( Params.driver==None ):
        #ドライバーとの接続確立
        #リモートブラウザを立ち上げる
        if( Params.PlatformName() == BrEmv.PlatformAndroid ):
            from process.matrix.modules.BrowserControl.CreateAppiumDriver import _Open
            _Open(Params)
        else:   #platformName": "windows"
            from process.matrix.modules.BrowserControl.CreateSeleniumDriver import _Open
            _Open(Params)

    #_sec=datetime.datetime.now().second
    #if((Params.driver !=None ) and ( _sec > 20 )):
    if(Params.driver ==None ):
        _e=NotLoginException(f'::BrOpen::取引システムと接続が切れています')
        raise _e

    #保存しているクッキーを読み込む
    try:
        _url=const.Tranding
        Params.driver.get( _url )

        if(Params.PlatformName()==BrEmv.PlatformWindows):
            #print("reopen aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            Params.Flags=Bit.Clr(Params.Flags,CFlags.B_DOWN)

            if( BrEmv.CookieUse ):
                try:
                    CCookieHandler.doRead(Params.driver)
                except InvalidCookieDomainException:
                    pass
                except Exception as e: # origin Exception
                    log.error( f'{getShortName(__name__)} CCookieHandler Error t:{type(e)} ') #e:{ e }')
                    #CCookieHandler.doDelete()
                finally:
                    Params.driver.get( _url )
                    pass    #Cookieエラーは無視する

        #画面サイズを取得する
        Params.bsize=bs.Get_bsize(Params,const.Min)

        # ログイン状態判定
        Params.driver.switch_to.frame(0)

        from process.matrix.modules.biWinning.GetResult import GetResult
        from process.matrix.modules.biWinning.__OnTrade1 import _doCreateCurrency

        for i in range(0,2):
            try:
                _value=GetResult(Params.driver,Params.bsize,False)
                Params.TradeSummary.SetAssets(_value)
                #print("Db更新します")
                Params.TradeSummary.doDbWrite(Params.Mode())
                Params.trade.Assets=_value
                Params.trade.Esti==CEsti.PASS
                Params.Flags=Bit.Clr(Params.Flags,CFlags.B_AMERR)

                #Params.Amount(const.Amount) #20220617 いらない

                _doCreateCurrency(Params.driver,False)
                break

            except NotLoginException as ne:
                from process.matrix.OnLogin import OnLogin
                OnLogin(Params,sts,evt)

    except ProcessContinuedException:
        Params.trade.Esti==CEsti.PASS
        #Params.driver =None
        pass
    except WebDriverException as _we:
        if(Params.PlatformName()==BrEmv.PlatformWindows):
            raise _we
        pass
        #Params.driver=None


@MatrixFunction
def BrClose(Params,sts,evt):

    if( Params.driver != None ):
        try:
            if( Params.PlatformName() == BrEmv.PlatformWindows ):
                #クッキーを保存する
                CCookieHandler().doWrite(Params.driver)
                pass
            
            #Params.driver.close()
            Params.driver.quit()
            if( Params.PlatformName() == BrEmv.PlatformWindows ):
                Params.driver = None
            log.error(f"driver close success!!")
        except Exception as e:
            log.error(f"driver close failed !! {e} ")
            Params.driver = None
            pass
        finally:
            pass
            #from data.enum import CFlags
            #import general.utility.bit as Bit
            #Params.Flags=Bit.Clr(Params.Flags,CFlags.B_DOWN)

@MatrixFunction
def BrRefresh(Params,sts,evt):

    try:
        #Params.driver.refresh()
        if( Params.driver != None ):
            Params.driver.get_window_size()
            log.error("driver refresh success!!")
        else:
            log.error("driver refresh skip !!")
    except Exception as e:
        _e= DriverDownException(f'::BrRefresh  failed !! e:{ e }')
        raise _e

def PageRefresh(driver):
    driver.get("data:,")
    driver.execute_script("window.open()")
    #driver.switch_to.window(driver.window_handles[1])
    #driver.get("data:,")
    driver.switch_to.window(driver.window_handles[0])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
