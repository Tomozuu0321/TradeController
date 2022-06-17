import os
import os.path as path
from data.environment.LivingFieldEnv.Folder import GrFolderDict as fenv
import pickle

class CCookieHandler():

    #メンバー変数
    __FOLDER__=path.join(fenv['data'],'cookies')
    __COOKIES_PATH__=path.join( __FOLDER__,'cookies.pickle')

    #cookieデータ読み込み
    @classmethod
    def doRead(cls,driver):
        if(os.path.isfile(cls.__COOKIES_PATH__)):
            cookies = pickle.load(open(cls.__COOKIES_PATH__,"rb"))
            for cookie in cookies:
                driver.add_cookie(cookie)
        return(driver)

    @classmethod
    #cookieデータ書き込み
    def doWrite(cls,driver):
        pickle.dump(driver.get_cookies(),open(cls.__COOKIES_PATH__,"wb"))

    @classmethod
    def doDelete(cls):
        if(os.path.isfile(cls.__COOKIES_PATH__)):
            os.remove(cls.__COOKIES_PATH__)
