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
def _ChangeCurrency( Params,driver,TypeIndex,TargetIndex,create=False ):

    _csslist=[
        [".sc-dwcuIR"       ,f".sc-eltcbb:nth-child({ TypeIndex }) > span",f".sc-aKZfe:nth-child( { TargetIndex }) > span","XXXXXXXXXXXXXXXXXXXXXXXXXXX" ],   # 2023/05/30 update
        [".sc-hLGeHF > span",f".sc-koaBLD:nth-child({ TypeIndex }) > span",f".sc-bKNyAY:nth-child({ TargetIndex }) > span:nth-child(2)",".sc-iaEFhd > span" ] # 2023/04/26 update
        #[".sc-dwcuIR"      ,".sc-eltcbb:nth-child(1) > span"  ,f".sc-aKZfe:nth-child({ TargetIndex }) > span","XXXXXXXXXXXXXXXXXXXXXXXXXXX" ],  # 2023/04/26 unfinished
        #[".sc-eWvPJL > span",".sc-dwcuIR:nth-child(1) > span",f".sc-iIEYCM:nth-child({ TargetIndex }) > span","XXXXXXXXXXXXXXXXXXXXXXXXXXX" ],  # 2022/06/22 unfinished
        #[".sc-iitrsy > span",".sc-eUWgFQ:nth-child(1) > span",f".sc-oHXjo:nth-child({ TargetIndex }) > span",".sc-hPCzgT:nth-child(1) span" ]   # 2022/06/22 update
    ]

    #if( _tests[0] ==const.LoginKey0 ) and ( _amount == 0.0 ):
    if( Params.bsize == CBSize.LARGE ) and ( create == False ):
        #print(_csslist[int(Params.bsize)][3])
        _element=driver.find_element(By.CSS_SELECTOR,_csslist[int(Params.bsize)][3] )
        #time.sleep(const.Sleep)
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

    # 2022/06/22 update
    if( _element.text == const.TargetCurrency ):
        log.critical( f" ChangeCurrency!! Nochg from {_element.text} to {const.TargetCurrency}") 
        return

    #_now=datetime.now()
    #print(f"::ChangeCurrency01 success {_now}")
    #time.sleep(const.Sleep)         # 2023/04/26 comment out
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
        #_element = WebDriverWait(driver,6).until(EC.presence_of_element_located((By.CSS_SELECTOR,".sc-bKNyAY:nth-child(1) > span:nth-child(2)")))
        #print(f"id={ _csslist[int(Params.bsize)][2] }")
        #_element=driver.find_element(By.CSS_SELECTOR, ".sc-bKNyAY:nth-child(1) > span:nth-child(2)")
        #_element=driver.find_element(By.CSS_SELECTOR, ".sc-bKNyAY:nth-child(1) > span")
        _element.click()
        #time.sleep(const.Sleep)
    except Exception as e:
        #log.info(f"errr {e}")
        _e=Exception(f'::ChangeCurrency03 failed!! { e }')
        raise _e
    finally:
        pass

    _now=datetime.now()
    print(f"::ChangeCurrency03 success {_now}")


def _doCreateCurrency( Params,reload=False ):
    #import time
    #from selenium.webdriver.common.by import By

    try:
        if( reload ):
            #print("reload=======================================================================================================")
            Params.driver.get(const.Tranding)
            time.sleep(1)
            Params.driver.switch_to.frame(0)
            time.sleep(1)
        #else:
            #print("Not NOT NOT load=======================================================================================================")
            #if( Params.bsize == CBSize.LARGE ):

        _ChangeCurrency( Params,Params.driver,const.ItemTypeIndex,const.CurrencyIndex,True ) # 2023/05/31 update

    except Exception as e:
        _text=f'::_doCreateCurrency-001 failed!! { datetime.now() } { type(e) }'
        log.error(f'{_text}')
        raise e
        pass
    