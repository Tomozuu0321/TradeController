from datetime import datetime
import time
from data.enum import CBSize
from data.biWconst import const
from data.environment.LivingFieldEnv.BrowserEnv import BrEmv
from general.utility.logger import log
from data.Exceptions import NotLoginException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from process.matrix.modules.biWinning.ChangeCurrency import _ChangeCurrency

"""
def _doCreateCurrency( Params,driver,reload=False ):
    #import time
    #from selenium.webdriver.common.by import By
    try:
        if( reload ):
            #print("reload=======================================================================================================")
            driver.get(const.Tranding)
            time.sleep(1)
            driver.switch_to.frame(0)
            time.sleep(1)
        #else:
            #print("Not NOT NOT load=======================================================================================================")
        # 2023/04/25 update
        driver.find_element(By.CSS_SELECTOR, "svg:nth-child(4) > path").click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, ".sc-koaBLD:nth-child(1) > span").click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, ".sc-bKNyAY:nth-child(1) > span:nth-child(2)").click()

        # 2022/05/14 update
        driver.find_element(By.CSS_SELECTOR, ".sc-dCuYax").click()                              # 2022/05/14 update
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, ".sc-UwFXA:nth-child(5) > p").click()              # 2022/05/14 update
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, ".sc-jMlkEa:nth-child(1) .sc-jbiwVq").click()      # 2022/05/14 update

        driver.find_element(By.CSS_SELECTOR, ".sc-jacpsN").click()
        driver.find_element(By.CSS_SELECTOR, ".sc-fePcYi:nth-child(5) > p").click()
        driver.find_element(By.CSS_SELECTOR, ".sc-gmmXTR:nth-child(1) .sc-gmAETw").click()

    except Exception as e:
        _text=f'::_doCreateCurrency-001 failed!! { datetime.now() } { type(e) }'
        log.error(f'{_text}')
        raise e
        pass
"""


#@MatrixSupportFunction
def __PrepareTrading(Params,driver,Amount ):

    isDown=True
    _e=None

    for i in range(0,3):
        try:
            _ChangeCurrency( Params,Params.driver,const.CurrencyIndex )
            isDown=False
            break
        except Exception as e:
            log.error(f'::PrepareTrading-001 failed retry c:{i}{ type(e) }')
            """
            if( Params.bsize == CBSize.LARGE ):
                try:
                    _doCreateCurrency( Params,True )
                    continue
                except Exception:
                    pass
            """
            _e=NotLoginException(f'::PrepareTrading-001 failed c:{i}{ type(e) }')
            #_e=DriverDownException(f'::PrepareTrading-001 failed c:{i}{ type(e) }')
            time.sleep(const.Sleep)     #これは必要なんだろうか

    if( isDown ):
        if(_e==None):
            _e=NotLoginException(f'::PrepareTrading-002 failed i:{i} d:{ isDown }')
            #_e= DriverDownException(f'::PrepareTrading-002 failed i:{i} d:{ isDown }')
        raise _e

    #取引通貨設定

    _csslist=[
        [".sc-hDjjHo","amount" ],   # 2022/05/14 update
        ["XXXXXXXXXX","amount" ]    # 2022/05/14 update
        #[".sc-ekBFwZ","amount" ],
        #[".sc-gGiJkG","amount" ]
    ]

    #time.sleep( 1 )
    #driver.switch_to.frame(0)

    #if( Params.bsize == CBSize.SMALL ):
    if( Params.bsize == CBSize.SMALL ) and ( Params.PlatformName() == BrEmv.PlatformAndroid ):
        isDown=True
        _e=None
    """
        for i in range(0,5):
            #print( f"cnt {i} {datetime.now()}") 
            try:
                time.sleep(const.Sleep+1)     #これは必要なんだろうか
                #signal.setitimer(signal.ITIMER_REAL, 0.5, 0.5)
                #_element = WebDriverWait(driver,15).until(EC.presence_of_element_located((By.CSS_SELECTOR,_csslist[int(Params.bsize)][0] )))
                _element = WebDriverWait(driver,6).until(EC.visibility_of_element_located((By.CSS_SELECTOR,_csslist[int(Params.bsize)][0] )))
                #_element = WebDriverWait(driver,15).until(EC.visibility_of_element_located((By.CSS_SELECTOR,".sc-ekBFwZ" )))
                #log.info(  _element.text)
                time.sleep(const.Sleep)     #これは必要なんだろうか
                _element.click()
                isDown=False
                #print( f" scss {i} {datetime.now()}") 
                break
            except Exception as e:
                log.error(f":PrepareTrading-003 failed retry {i} {datetime.now()} t:{type(e)}")
                _e=NotLoginException(f':PrepareTrading-003 failed  i:{i} t:{type(e)}')
                #time.sleep( 1 )
            finally:
                pass
        if( isDown ):
            if(_e==None):
                _e=NotLoginException(f':PrepareTrading-003 failed  i:{i} d:{ isDown }')
                #_e= DriverDownException(f':PrepareTrading-003 failed  i:{i} d:{ isDown }')
            raise _e
    """
    if( _e != None ):
        print( f"::PrepareTrading-003 success {i} {datetime.now()}") 

    #"""
    #time.sleep( 10 )
    #driver.find_element(By.CSS_SELECTOR, ".sc-ekBFwZ").click()

    #log.error(f"価格タブを取る！！{datetime.now()} start {1}")
    try:
        ele="__PrepareTrading err"
        ele = WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.NAME,_csslist[int(Params.bsize)][1] )))
        #ele = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME,_csslist[int(Params.bsize)][1] )))
        #ele.clear()
        #log.error( f"name OK css {datetime.now()} { type(ele)}" )
    except TimeoutException as _te:
        log.error(f"タイムアウト発生！！{datetime.now()} errr002-1 {type(_te)}")
        raise _te

    except Exception as e:
        log.error(f"間に合ってないよ！！{datetime.now()} errr002 {type(e)}")
        _e=NotLoginException(f'::PrepareTrading Not Login { type(ele) }')
        raise _e
        return
    finally:
        pass

    #print( f"::PrepareTrading-004 success {datetime.now()}") 

    #time.sleep(const.Sleep)
    #driver.find_element(By.CSS_SELECTOR, ".sc-ekBFwZ").click()
    #time.sleep(const.Sleep)

    #投資金額を入れる所まで
    val=f"¥{int(Amount)}"
    #print(val)
    #ele=driver.find_element(By.NAME, "amount")
    #text = ele.get_attribute('value')
    #print( text )
    _key=_csslist[int(Params.bsize)][1] 
    for i in range(0,10):
        ele=driver.find_element(By.NAME, _key )
        if type(ele) !=None :
            break
        else:
            time.sleep(const.Sleep)     #これは必要なんだろうか

    for i in range(0,10):
        try:
            #ele=driver.find_element(By.NAME, "amount")
            text=ele.get_attribute('value')

            #if(text.startswith('$')):
                #_e=NotLoginException(f'::PrepareTrading-005 Not Login { text }')
                #raise _e

            #print(f'len {len(text)} {text} {datetime.now()}')
            if text == '¥0':
                ele.send_keys(Keys.RIGHT)
                ele.send_keys(Keys.RIGHT)
                ele.send_keys(val)
                #print(f'barek {i} { len(text)} {datetime.now()}')
                break
            else:
                ele.send_keys(Keys.CONTROL + "a")
                time.sleep(const.Sleep*2)     #これは必要なんだろうか
                ele.send_keys(Keys.DELETE)
                #ele.clear()
                #time.sleep(const.Sleep)     #これは必要なんだろうか
                #ele.send_keys(Keys.DELETE)
                #ele.send_keys(Keys.DELETE)
                #time.sleep(const.Sleep)     #これは必要なんだろうか
                #for i in range(len(text)):
                #ele.sendKeys(Key_s.BACK_SPACE)
                continue

        except NotLoginException as _ne:
             raise _ne

        except Exception as e:
            log.error(f'::PrepareTrading-005 failed retry c:{i}{ type(e) } {datetime.now()}')
            #time.sleep(1)

    if( Params.PlatformName() == BrEmv.PlatformAndroid ):
        ele.clear()

    #print( f"::PrepareTrading-005 success {datetime.now()}") 
