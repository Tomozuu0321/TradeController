from urllib3.exceptions import MaxRetryError
from data.enum import CFlags
from data.biWconst import const
from data.Exceptions import DriverDownException #,NotLoginException
from process.matrix.modules.BrowserControl.Header import webdriver,options
from general.utility.logger import MatrixSupportFunction,log
import general.utility.bit as Bit
from general.utility.StopWatch import StopWatchEx

@StopWatchEx("_Open")
@MatrixSupportFunction
def _Open(Params):
    try:
        url=Params.GetUrlEx(0,1,0)
        # http://%s:%s/wd/hub  =>http://%s:%s/wd/hub/だと起動しない

        #from process.matrix.modules.BrowserControl.HttpSessionCheck import _HttpSessionCheck
        #_HttpSessionCheck(url)

        # Selenium Serverに接続
        driver = webdriver.Remote(\
                    command_executor=url,\
                    options=options)

        driver.set_window_position(0, 0)
        driver.set_window_size(const.width,const.Height)
        #driver.set_window_position(100,100)
        #driver.set_window_size(500, 800)
        #driver.set_window_size(1500, 1020)
        Bit.Clr(Params.Flags,CFlags.B_DOWN)
        Params.driver=driver

    except MaxRetryError as me:
        _e= DriverDownException(f'{__name__} open failed !! e:{ me }')
        raise _e
