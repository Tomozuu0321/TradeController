# %%
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# %%
from general.utility.logger import MatrixSupportFunction,log
from data.biWconst import const
from data.TradeInfo import CTrade
from data.enum import CBSize
import general.utility.bsize as bs

@MatrixSupportFunction
def _OneClickTrade( Params,driver ):

    _csslist=[
      #[ ".sc-hcevGK",".sc-jYCGvq",".sc-bAfeAT",".sc-bOdqNl", ],
      [ ".sc-hcevGK",".sc-kGNybE",".sc-bAfeAT",".sc-bOdqNl",".sc-ekBFwZ" ],
      [ ".sc-fcmPfK",".sc-ctaXAZ",".sc-dFJsGO",".sc-bOdqNl",".sc-ekBFwZ" ]
    ]
    
    _currnt=driver.current_url
    log.error( f"_OneClickTrade cr { _currnt } " )

    _url=const.Home + const.Tranding
    if( _url != _currnt ):
        pass

    driver.get( _url )
    driver.switch_to.frame(0)

    if( Params.bsize == CBSize.SMALL ):
        #driver.find_element(By.CSS_SELECTOR, ".sc-ekBFwZ").click()
        driver.find_element(By.CSS_SELECTOR, _csslist[0][4]).click()
    
    _elements=driver.find_elements(By.CSS_SELECTOR,_csslist[int(Params.bsize)][0])
    if( len(_elements) != 0 ):
        log.error( _elements[0].get_attribute('innerHTML'))
        _elements=driver.find_elements(By.CSS_SELECTOR,_csslist[ int(Params.bsize) ][2])
        driver.find_element(By.CSS_SELECTOR,_csslist[ int(Params.bsize) ][2]).click()
        """
        if( len(_elements) != 0 ):
            _elements[0].click()
        #driver.find_element(By.CLASS_NAME,_csslist[ int(Params.bsize) ][2]).click()
        """
    else:
        driver.find_element(By.CSS_SELECTOR,_csslist[ int(Params.bsize) ][1]).click()
        """
        if( len(_elements) != 0 ):
            for i in range( len(_elements)):
                log.error( _elements[0].get_attribute('innerHTML'))
            
            #ctions = ActionChains(driver)
            #ctions.move_to_element(_elements[0]).perform()
            #ctions.click().perform()
            _elements[0].click()
        """