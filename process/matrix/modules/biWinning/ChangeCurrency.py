# %%
from datetime import datetime
import time
#from matplotlib.pyplot import bar_label
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from data.Exceptions import NotLoginException
from data.enum import CBSize

# %%
#import time
from general.utility.logger import log #,MatrixSupportFunction,log
#import general.utility.bsize as bs
#from data.biWconst import const
#import general.utility.bsize as bs
from data.biWconst import const
from general.utility.StopWatch import StopWatch

#@MatrixSupportFunction
#@StopWatch
def _ChangeCurrency( Params,driver,TargetIndex ):

    _csslist=[
        [".sc-eWvPJL > span",".sc-dwcuIR:nth-child(1) > span",f".sc-iIEYCM:nth-child({ TargetIndex }) > span","XXXXXXXXXXXXXXXXXXXXXXXXXXX" ],  # 2022/06/22 unfinished
        [".sc-iitrsy > span",".sc-eUWgFQ:nth-child(1) > span",f".sc-oHXjo:nth-child({ TargetIndex }) > span",".sc-hPCzgT:nth-child(1) span" ]   # 2022/06/22 update
        #[".sc-eWvPJL > span",".sc-dwcuIR:nth-child(1) > span",f".sc-iIEYCM:nth-child({ TargetIndex }) > span"], # 2022/05/14 update
        #[".sc-hPCzgT:nth-child(1) span",".sc-dYzljZ:nth-child(1) > span",f".sc-hcevGk:nth-child({ TargetIndex }) > span"]  # 2022/06/09 update
    ]

    if( Params.bsize == CBSize.LARGE ):
        _element=driver.find_element(By.CSS_SELECTOR,_csslist[int(Params.bsize)][3] )
        time.sleep(const.Sleep)
        _element.click()

    #画面データにアクセス可能になるまで待機する
    try:
        _element = WebDriverWait(driver,6).until(EC.presence_of_element_located((By.CSS_SELECTOR,_csslist[int(Params.bsize)][0] )))
    except Exception as e:
        log.error(f'::ChangeCurrency01 failed retry { type(e) }')   #log.info(f"errr {e}")
        _e=Exception(f'::ChangeCurrency01 failed!! { type(e) }')
        raise _e
    finally:
        pass

    # 2022/06/09 update
    if( _element.text != const.TargetCurrency ):
        pass
        #if( Params.bsize == CBSize.LARGE ):
        #    _e=Exception(f'::ChangeCurrency03 Large failed!! { _element.text }')
        #    raise _e
    else:
        """
        #if( Params.bsize == CBSize.SMALL ):
            #if( _element.text == const.TargetCurrency ):
                log.error( f" ChangeCurrency!! Nochg from {_element.text} to {const.TargetCurrency}") 
                return
        """
        pass

    #_now=datetime.datetime.now()
    #print(f"::ChangeCurrency01 success {_now}")
    time.sleep(const.Sleep)         #ここは確定
    _element.click()

    #if( Params.bsize == CBSize.LARGE ):
    #    #log.error( f" ChangeCurrency!! Large finish!! {datetime.now()} ") 
    #    return

    #_now=datetime.datetime.now()
    #print(f"::ChangeCurrency01-C success {_now}")
    #log.error( f" ChangeCurrency!! Change { datetime.now() } from {_element.text} to {const.TargetCurrency}") 

    #仮想通貨グループを選択
    try:
        #driver.find_element(By.CSS_SELECTOR, _csslist[int(Params.bsize)][1] ).click()
        _element = WebDriverWait(driver,6).until(EC.presence_of_element_located((By.CSS_SELECTOR,_csslist[int(Params.bsize)][1] )))
        _element.click()
        #time.sleep(const.Sleep)
    except Exception as e:
        #log.info(f"errr {e}")
        _e=Exception(f'::ChangeCurrency02 failed!! { e }')
        raise _e
    finally:
        pass
    
    #now=datetime.datetime.now()
    #print(f"::ChangeCurrency02 success {_now}")

    #time.sleep(2)
    try:
        #driver.find_element(By.CSS_SELECTOR, _csslist[int(Params.bsize)][1] ).click()
        #driver.find_element(By.CSS_SELECTOR, _csslist[int(Params.bsize)][ TargetIndex ] ).click()
        _element = WebDriverWait(driver,6).until(EC.presence_of_element_located((By.CSS_SELECTOR,_csslist[int(Params.bsize)][2])))
        _element.click()
        #time.sleep(const.Sleep)
    except Exception as e:
        #log.info(f"errr {e}")
        _e=Exception(f'::ChangeCurrency03 failed!! { e }')
        raise _e
    finally:
        pass

    #_now=datetime.datetime.now()
    #print(f"::ChangeCurrency03 success {_now}")

    