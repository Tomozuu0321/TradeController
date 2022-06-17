# %%
import requests
import urllib
import pickle
from general.utility.logger import log
#from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPClient

# %%
#辞書雛形作成
def doCreate(key,value):
    _dic=dict={'MT':[{'Evt': key,key:value}]}
    return(_dic)

def doRequest( key,value,url ):

    print("call doRequest St ")
    _dic= doCreate(key,value)

    _post_data = urllib.parse.quote(pickle.dumps(_dic))
    #_url = Params.GetUrlEx(0,0,1)
    _url = "http://localhost:8888/wd/hub/"
    try:
        """
        http_client = HTTPClient() #AsyncHTTPClient()
        #http_client = AsyncHTTPClient()
        headers = {'Content-Type': 'application/json'}
        response = http_client.fetch(_url,
               raise_error=False,
               method='POST',
               body=_post_data,
               headers=headers)
        """
        #response = requests.post(url,json=_post_data)
        #log.debug(response)
        #log.debug(response.headers.get('Content-Type'))
        pass
    except Exception as e: # origin Exceptionexcept:
        log.error(f'Error ::requests {e}')
    finally:
        pass

    print("call doRequest ed ")

