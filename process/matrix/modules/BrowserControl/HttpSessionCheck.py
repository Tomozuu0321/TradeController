from urllib3.util.retry import Retry
from urllib3.exceptions import MaxRetryError
#from requests.packages.urllib3.util.retry import Retry
import requests
from requests.adapters import HTTPAdapter
from data.environment.LivingFieldEnv.BrowserEnv import BrEmv
from general.utility.logger import MatrixSupportFunction,log
from general.utility.StopWatch import StopWatch

#@MatrixSupportFunction
@StopWatch
def _HttpSessionCheck(url):

    try:
        s = requests.Session()
        _url=url+'/status'

        retries = Retry(total=5,
                    backoff_factor=1,
                    status_forcelist=[ 500, 502, 503, 504 ])

        s.mount('https://', HTTPAdapter(max_retries=retries))
        s.mount('http://', HTTPAdapter(max_retries=retries))
        print(BrEmv.HttpSessionCheck)
        r = s.request('GET', _url, timeout=BrEmv.HttpSessionCheck )
        r.raise_for_status()
        log.error(f'{__name__} success !! t:{type(r)} e:{ r }')  #{r.text}')

    except Exception as e:
        _SessionErrorHandler(_url,e )

def _SessionErrorHandler( url,e):
    #_e= MaxRetryError(url,f'{__name__} failed !! t:{type(e)} e:{ e }r:{e.response}')
    _e= MaxRetryError(url,f'{__name__} failed !! t:{type(e)}') #e:{ e }r:{e.response}')
    raise _e
