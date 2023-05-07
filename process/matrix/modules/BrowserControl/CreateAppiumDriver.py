from data.enum import CFlags
from data.Exceptions import DriverDownException,NotLoginException
import general.utility.bit as Bit
from process.matrix.modules.BrowserControl.Header import webdriver,options
from general.utility.logger import MatrixSupportFunction,log
from selenium.common.exceptions import WebDriverException,NoSuchElementException

@MatrixSupportFunction
def _Open(Params):

    if(Bit.Chk(Params.Flags,CFlags.B_DOWN)):
        _e= NotLoginException(f'{__name__}-001 open skip !! ')
        raise _e

    caps = webdriver.DesiredCapabilities.CHROME.copy()
    caps["platformName"] = "Android"
    caps["deviceName"] = "000000"
    caps["automationName"]="UiAutomator2"
    caps["browserName"] = "Chrome"
    #caps["noReset"]="true"

    url=Params.GetUrlEx(0,0,2)

    caps["noReset"]="true"
    options.add_experimental_option("androidKeepAppDataDir",True)

    # appium Serverに接続
    try:
        driver = webdriver.Remote( command_executor=url,\
                               desired_capabilities=caps,options=options)

        Params.driver=driver

        """
        _current = driver.current_window_handle
        _Handles = driver.window_handles

        for i in range(0,len(driver.window_handles)-1) :
            driver.switch_to.window(driver.window_handles[i]).close()

        Params.driver=driver


        try:
            driver.quit()
        except WebDriverException as we:
            pass

        Params.driver=driver
        driver.get("data:," )
        #driver.switch_to.window(driver.window_handles[i]).
        """
    except DriverDownException as de: # ここで入って来たという事は整合性がとれたという事
        pass

    except WebDriverException as we: # ここで入って来たという事は整合性がとれたという事
        try:
            #from data.enum import CSysFlags
            #import general.utility.bit as _Bit
            Params.Flags=Bit.Clr(Params.Flags,CFlags.B_DOWN)
            """
            from process.matrix.modules.BrowserControl.BrowserControls import BrClose
            Params.driver=webdriver.Remote
            BrClose(Params,Params.sts(),Params.evt())
            pass
            #webdriver.Remote.get("https://www.google.co.jp/")
            #webdriver.Remote.close()
            """
        except Exception:
            pass
        pass

    except Exception as e: # origin Exception
        from process.matrix.modules.BrowserControl.BrowserControls import BrClose
        BrClose(Params,Params.sts(),Params.evt())
        Params.driver=None
        print(f'{__name__} open failed !! e:{ type(e) }')
        #_e=NotLoginException(f'::PrepareTrading-005 Not Login { text }')
        #_e= DriverDownException(f'{__name__} open failed !! e:{ type(e) }')
        _e= NotLoginException(f'{__name__} open failed !! e:{ type(e) }')
        raise _e
