import time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from data.enum import CBSize
from general.utility.logger import log #,MatrixSupportFunction,log
from data.biWconst import const
from data.Exceptions import NotLoginException,DriverDownException
from general.utility.StopWatch import StopWatch

def _ChangeTime( Params,driver,TimeIndex ):

    _csslist=[
        [".expiration > span",f".sc-iBaPrD:nth-child({ TimeIndex }) .time" ],
        [".expiration > span",f".sc-iBaPrD:nth-child({ TimeIndex }) .time" ]
    ]

    #画面データにアクセス可能になるまで待機する
    try:
        _element = WebDriverWait(driver,6).until(EC.presence_of_element_located((By.CSS_SELECTOR,_csslist[int(Params.bsize)][0] )))
    except Exception as e:
        print(f'::ChangeTime01 failed!!!! { type(e) }')
        _e=DriverDownException(f'::ChangeTime01 failed!!!! { type(e) }')
        raise _e
    finally:
        pass

    _minstr=f"{TimeIndex} min"
    _getText=_minstr
    #print( f"minstr={_minstr}")
    try:
        _getText=_element.get_attribute('innerHTML')
        #print(f"gertext={_getText}")
    except Exception as e:
        #print(f"errror")
        pass
    # 取得した数字が引数と一致している場合は何もしない
    if( _getText == _minstr ):
        log.critical( f" ChangeTimey!! Nochg from { _getText } to {_minstr}")
        return

    _element.click()
    _element.click()
    #time.sleep(const.Sleep)
    
    #時間項目を選択
    isDown=True
    _e=None

    for i in range(0,3):
        try:
            #driver.find_element(By.CSS_SELECTOR,_csslist[Params.bsize][1] ).click()
            _element = WebDriverWait(driver,6).until(EC.presence_of_element_located((By.CSS_SELECTOR,_csslist[int(Params.bsize)][1] )))
            _element.click()
            #time.sleep(const.Sleep)
            isDown=False
            break
        except Exception as e:
            print(f'::ChangeTime02 failed!!!! retry c:{i}{ type(e) }')
            _e=DriverDownException(f'::ChangeTime02 failed failed c:{i}{ type(e) }')
            time.sleep(const.Sleep)     #これは必要なんだろうか

    if( isDown ):
        if(_e==None):
            #_e=Exception(f'::ChangeTime02 failed failed i:{i} d:{ isDown }')
            _e=DriverDownException(f'::ChangeTime03 failed failed c:{i}{ type(e) }')
        raise _e

    #pass
    #now=datetime.datetime.now()
    #print(f"::ChangeTime02 success {_now}")

    _now=datetime.now()
    print(f"::ChangeTime03 success {_now}")
