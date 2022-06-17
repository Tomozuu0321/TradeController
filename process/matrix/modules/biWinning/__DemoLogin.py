# %%
import time
from general.utility.logger import MatrixSupportFunction,log
from data.biWconst import const
from data.TradeInfo import CTrade
from data.enum import CBSize
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
    _elements=driver.find_element_by_class_name(_csslist[1][0]).find_elements(By.CSS_SELECTOR,_csslist[1][1])

    # %%
    if( len(_elements) ):
        #print("demo st")
        print( f"{__name__} typ:{type(_elements[0])} ")
        log.error(f"{__name__} {_elements[0].get_attribute('innerHTML')} get suc\cess")
        ctions = ActionChains(driver)
        ctions.move_to_element(_elements[0]).perform()
        ctions.click()
        ctions.perform()
        driver.switch_to.alert.accept()
        #_elements[0].click()
        print( f"{__name__} demo ed")
    else:
        print(f"{__name__} demo err get failed !!" )

    #クッキーを更新する
    CCookieHandler().doWrite(Params.driver)


    
