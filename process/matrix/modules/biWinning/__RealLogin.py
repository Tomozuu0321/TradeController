from general.utility.logger import MatrixSupportFunction,log
from data.biWconst import const

@MatrixSupportFunction
def _Nop(Params,driver):

    #履歴からアカウント情報が引き継がれる筈
    _url=const.Home+ const.Tranding
    #log.info(f'top url~{_url}')
    #Params.driver.get( _url )

@MatrixSupportFunction
def _login(Params,driver):
    _url=const.Home+const.Tranding
    #log.info(f'top url~{_url}')
    #Params.driver.get( _url )

