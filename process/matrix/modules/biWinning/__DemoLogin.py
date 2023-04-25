# %%
import time
from datetime import datetime
from data.enum import CBSize
from data.biWconst import const
from general.utility.logger import log,MatrixSupportFunction
from general.data.TradeInfo import CTrade
import general.utility.bsize as bs
from data.cookies.CookieHandler import CCookieHandler

# %%
#from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

@MatrixSupportFunction
def _Nop(Params,driver):

    #履歴からアカウント情報が引き継がれる筈
    _url=const.Home+ const.Tranding
    print(_url)
    #log.info(f'top url~{_url}')
    #Params.driver.get( _url )

@MatrixSupportFunction
def _login(Params,driver):

    # %%
    #https://www.bi-winning.org/#/demo
    #driver=Params.driver

 #   _url=const.Home + "/#" 
 #   driver.get( _url )

    if( driver==None ):
        return

    _url=const.Home + "/#/demo" 
    _url

    #クッキーを初期化する
    driver.delete_all_cookies()
    CCookieHandler.doDelete()

    # %%
    #const.Tranding
    driver.get( _url )

    # %%
    _csslist=[
        ["resources-landing",".btn-square" ],
        ["resources-landing",".btn-square" ]
    ]
    try:
        _elements=driver.find_elements(By.CSS_SELECTOR,_csslist[1][1])   # 2023/04/22 update
        #_elements=driver.find_element_by_class_name(_csslist[1][0]).find_elements(By.CSS_SELECTOR,_csslist[1][1])
        #self.driver.find_element(By.CSS_SELECTOR, ".btn-square").click()
        # %%
        if( len(_elements) ):
            #print("demo st")
            #"""
            #print( f"{__name__} typ:{type(_elements[0])} ")
            #log.error(f"{__name__} {_elements[0].get_attribute('innerHTML')} get success")
            ctions = ActionChains(driver)
            ctions.move_to_element(_elements[0]).perform()
            ctions.click()
            ctions.perform()
            driver.switch_to.alert.accept()
            #"""
            #_elements[0].click()
            #log.critical( f'::__DemoLogin-001 success { datetime.now()}')
        
        #クッキーを更新する
        CCookieHandler().doWrite(Params.driver)

    except Exception as e:
        _text=f'::__DemoLogin-001 failed!! { datetime.now() } { type(e) }'
        log.error(f'{_text}')
        pass

