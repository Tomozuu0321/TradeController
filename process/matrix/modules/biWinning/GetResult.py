# %%
from datetime import datetime
import time
from data.enum import CBSize
from data.biWconst import const
from general.utility.logger import log
#from general.utility.bsize import Get_bsize
#from data.biWconst import CbiWconst
from data.Exceptions import NotLoginException,ProcessContinuedException
#from data.Exceptions import NotLoginException
from general.utility.StopWatch import StopWatch
#import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import WebDriverException
#from data.cookies.CookieHandler import CCookieHandler

# %%
@StopWatch
def GetResult( driver,bsize,isAmountTest ):
#sc-jUEnpm
#
    def pageInit( driver,i,max ):
        if(i==0):
            time.sleep(const.Sleep)     #これは必要なんだろうか
        else:
            driver.get(const.Tranding)
            time.sleep(1)
            driver.switch_to.frame(0)
            time.sleep(const.Sleep)     #これは必要なんだろうか
            pass

    """
    def pageInit( driver,i,max ):
        if( i >= (max -1 )):
            if( isReset ):
                driver.delete_all_cookies()
                CCookieHandler.doDelete()
            else:
                return
        if(i>0):
            driver.get(const.Tranding)
            time.sleep(1)
            driver.switch_to.frame(0)
            #time.sleep(1)
        else:
            time.sleep(2)
    """
    
    _csslist=[
        #sc-jMScns
        [".sc-ezront","XXXXXXXXXXXXXXXXXX"],        # 2022/06/09 update
        [".sc-jQbIHB","XXXXXXXXXXXXXXXXXX"],        # 2022/06/09 update  idx=1はもう使ってない
        #[".sc-gJrzqj",".sc-iuGMqu > span"],        # 2022/05/14 update
        #[".sc-jUEnpm",".sc-jUEnpm > span"],        # 2022/05/14 update
    ]

    #残額が表示されていない場合　ログインしてないので以降の処理をスキップする
    _elements=[]
    _amount=const.InvalidValue
    _max=3
    _Result=const.InvalidValue
    _tests=["test","$-1000"]

    for i in range(0,_max):    #5->2 上手くとれる時は一発だから
        #画面データにアクセス可能になるまで待機する
        try:
            pageInit( driver,i,_max)
            #time.sleep(const.Sleep)     #これは必要なんだろうか
            _element = WebDriverWait(driver,6).until(EC.presence_of_element_located((By.CSS_SELECTOR,_csslist[int(bsize)][0] )))

            if( type(_element) == WebElement ):
                log.error(f':GetResult-001 _element get  success { datetime.now()} ---------------------------------')
                #print( _element.get_attribute('innerHTML'))
                #_elements=_element.find_elements_by_tag_name("span")
                #_elements=_element.find_elements_by_tag_name("div")
                _elements=_element.find_elements(By.TAG_NAME,"div")
                if( len(_elements) != 0 ):
                    if( bsize == CBSize.SMALL ):
                        _tests=_elements[2].text.translate(str.maketrans({',':'','¥':'',' ':''})).splitlines()
                    else: # (Params.bsize == CBSize.LARGE ):
                        _tests=_elements[9].text.translate(str.maketrans({',':'','¥':'',' ':''})).split(":")

                    #投資額が0円の場合　ループを抜ける
                    _amount=float(_tests[1])
                    if( _tests[0] ==const.LoginKey0 ) and ( _amount == 0.0 ):
                        break
                    else:
                        # ここに入ってくるという事は購入が間に合ってなくて１分取引になってしまったという事
                        log.error(f':GetResult-001 not matchs({i}) retry a:{ _amount } { datetime.now()} --------- ')
            else:
                log.error(f':GetResult-001 _element Nome retry { datetime.now() }')

        except TimeoutException as _te:
            if( i >=(_max-1)):
                _text=f":GetResult-001 TimeoutException catch!! ログインしてない {datetime.now()}"
                log.error(f'{_text}')
                _e=NotLoginException(f'{_text}')
                raise _e
            else:
                log.error(f':GetResult-001 TimeoutExceptions({i}) retry { datetime.now() } { type(_te) }')
                pass

        except WebDriverException as _we:
            _text=f'::GetResult WebDriverException catch!! a:{ _amount } { datetime.now()}'
            log.error( f'{_text} a:{ _amount } { datetime.now()}')
            #_pc=ProcessContinuedException( f'{_text}')
            #raise _pc
            raise _we

        except Exception as e:
            if( i >=(_max-1)):
                _text=f':GetResult-001 failed!! { datetime.now() }'
                log.error(f'{_text}')
                _e=Exception(f'{_text } {type(e)}')
                raise _e
            else:
                log.error(f':GetResult-001 faileds({i}) retry { datetime.now() } { type(e) }')
                pass

    #
    # 以下要素が取得できている場合の処理
    #
    if( _amount > 0.0 and isAmountTest ):
        #投資額が残っている場合はisReset要求なしの場合　つまりopenからよばれてない場合　例外を投げる
        _text=f'::GetResult-ProcessContinue a:{ _amount } { datetime.now()}'
        log.error( f'{_text} a:{ _amount } { datetime.now()} --------- ')
        _pc=ProcessContinuedException( f'{_text}')
        raise _pc

    if( bsize == CBSize.SMALL ):
        _tests=_elements[0].text.translate(str.maketrans({',':'','¥':'',' ':''})).splitlines()

    else: # (Params.bsize == CBSize.LARGE ):
        _tests=_elements[8].text.translate(str.maketrans({',':'','¥':'',' ':''})).split(":")

    _Result=const.InvalidValue
    if( len( _tests ) > 1 ):
        if( _tests[0] ==const.LoginKey1 ):
            _Result=float(_tests[1])

    print( f"::GetResult success({i}) { _tests[0] } r:{_Result} a:{_amount} {datetime.now()} {type(_Result)}") 

    return(_Result)
