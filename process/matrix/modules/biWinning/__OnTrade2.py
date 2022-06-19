from datetime import datetime
import time
import re
from data.enum import CBSize,CFlags,CEsti
from data.biWconst import const
#from data.environment.LivingFieldEnv.BrowserEnv import BrEmv
from general.utility.logger import MatrixSupportFunction,log
#import general.utility.bsize as bs
import general.utility.bit as Bit
#from data.Exceptions import  DriverDownException,NotLoginException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
#from selenium.webdriver.common.keys import Keys
#from process.matrix.modules.biWinning.ChangeCurrency import _ChangeCurrency

@MatrixSupportFunction
def __OnReject(Params,driver,Tra ):

    print("hallow __OnReject ")
    Params.Flags=Bit.Clr(Params.Flags,CFlags.REJECT)
    return

# %%
#@MatrixSupportFunction
def __OnTrade(Params,driver,Tra ):

    if( Tra.Issimulate ):
        _text=f"::__OnTrade-002 シュミレートモードです {datetime.now()}"
        Params.Msg=_text
        log.critical(_text)
        return

    #driver.find_element ele.get_attribute('value')
    #print( "購入を開始します" )
    
    def MakeMessage(html):
        return(re.findall(r'<span*>(.*)</span>',html)[0])
    
    _now=datetime.now()
    if( _now.second > 29 ):
        print(f"tra Cancel {_now}")
        return

    _csslist=[
        #".sc-iJmhdZ > .dp__caption").click()
        #".sc-fSnZzA > .dp__caption").click()
        [".sc-gfHAkt > .dp__caption",".sc-hcevGk > .dp__caption",".sc-kNPvCX",".sc-cqtpGg"],    # 2022/06/09 update 未対応
        [".sc-iJmhdZ > .dp__caption",".sc-fSnZzA > .dp__caption",".sc-kMOkjD","xxxxxxxx"],   # 2022/06/09 update
        #[".sc-gfHAkt > .dp__caption",".sc-hcevGk > .dp__caption",".sc-kNPvCX",".sc-cqtpGg"],   # 2022/05/14 update
        #[".sc-eTLWQi > .dp__caption",".sc-fcmPfK > .dp__caption",".sc-bQVmPH",".sc-jnHOtz"],   # 2022/05/14 update
    ]

    # Buy or Sell 
    #print(f"購入を開始します {datetime.now()}")
    idx=-1;
    #とりあえず順張りロジック
    if( Tra.Esti==CEsti.Buy or Tra.Esti==CEsti.RBuy ):
        idx=0
        #idx=1
        #driver.find_element(By.CSS_SELECTOR,_csslist[int\(Params.bsize)][0] ).click()
        #print("buy")
    elif( Tra.Esti==CEsti.Sell or Tra.Esti==CEsti.RSell ):
        idx=1
    else:               #Tra.Esti==CEsti.PASS
        Params.trade.SummaryFlags=CFlags.SUCCESS
        _text=f"::__OnTrade-001 購入をスキップしました {datetime.now()}"
        Params.Msg=_text
        log.critical(_text)
        return

    try:
        _element = WebDriverWait(driver,8).until(EC.presence_of_element_located((By.CSS_SELECTOR,_csslist[int(Params.bsize)][idx] )))
        time.sleep(const.Sleep)     #これは必要なんだろうか
        _element.click()

    except Exception as e:
        _text=f"::__OnTrade-003 エラーによりボタンのクリックに失敗しました {datetime.now()} { type(e) }"
        Params.Msg=_text
        log.critical(_text)
        return

    finally:
        pass
    
    #_now=datetime.now()
    #print(f"tra success {_now}")

    try:
        #2022/6/17 to 6->10
        _element = WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.CSS_SELECTOR,_csslist[int(Params.bsize)][2] )))
        #_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,_csslist[int(Params.bsize)][2] )))
        _getText=_element.get_attribute('innerHTML')

        #if( const.RejectWord in _getText ):
        if( const.SuccessWord in _getText ):
            _msg=MakeMessage(_getText)
            _text=f" {_msg} { datetime.now().replace(microsecond = 0)}"
            Params.Msg=_text
            #print(f"_tra getmsg {_getText} {_msg}")
            Params.trade.SummaryFlags=CFlags.SUCCESS
            log.critical( f"::__OnTrade-001 {_text} ")

        elif( const.RejectWord in _getText ):
            _msg=MakeMessage(_getText)
            Params.Flags=Bit.Set(Params.Flags,CFlags.REJECT)
            test=f"::_OnTrade-001 取引システムに購入を拒絶されました f:0x{Params.Flags:x} {datetime.now()} { _getText }"
            Params.Msg= _msg
            Params.trade.SummaryFlags=CFlags.REJECT
            log.critical(_text)

        else: #購入失敗
            #_msg=MakeMessage(_getText)
            _text=f"::__OnTrade-001 購入に失敗しました f:0x{Params.Flags:x} {datetime.now()} T:{ _getText }"
            #print(f"_tra getmsg {_getText}")
            Params.Msg=_text
            log.critical(_text)

        if( Params.bsize == CBSize.SMALL ):
            driver.find_element(By.CSS_SELECTOR,_csslist[0][3] ).click()

    except TimeoutException as _te:
        _text=f"::__OnTrade-001 タイムアウトにより購入に失敗しました f:0x{Params.Flags:x} {datetime.now()} { type(_te) }"
        Params.Msg=_text
        log.critical(_text)

    except Exception as e:
        _text=f"::__OnTrade-001 エラーにより購入に失敗しました f:0x{Params.Flags:x} {datetime.now()} { type(e) }"
        Params.Msg=_text
        log.critical(_text)

    finally:
        #driver.find_element(By.CSS_SELECTOR,_csslist[0][3] ).click()
        pass

