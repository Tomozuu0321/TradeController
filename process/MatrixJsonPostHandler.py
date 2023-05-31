import os
import glob
#import pickle
import urllib
#import json
import ast
#import chardet

from data.enum import CSts,CEvt
from data.environment.LivingFieldEnv.Folder import GrFolderDict as fenv
from general.utility.logger import log
import general.utility.pickler as pp
#from general.utility.StopWatch import StopWatch

# %%
#
# 循環参照になってしまうのマトリクス処理には入れない
#
def OnRequest(Process,Params ):
   _files=glob.glob((fenv['Request']+'/*.pickle'))
   _files.sort(key=os.path.getmtime,reverse=False)
   _isExit=False
   for _file in _files :
      try:
         _data=pp.Deserialize(_file)
         _name=_data['MT'][0]["Evt"]
         _evt=CEvt[_name]
         #print( f"{_key}  typr{_key}" )
         if( type(_evt) == CEvt ):
            #Params.Receive=_data
            #self.MatrixHandler(owner,_evt)
            #Params.Receive=body
            _isExit=Process.MatrixJsonPostHandler( Process,_evt,_data )
            break
      except KeyError:
         log.error(" Key Error " )
      finally:
         os.remove(_file)
   return(_isExit)

"""
def getEncoding(str):
   result = chardet.detect(str)
   return result['encoding']
"""
# %%
#@StopWatch
def MatrixJsonPostHandler(Handle,Process):

   self=Handle
   _isExit=False
   if self.request.headers.get('Content-Type') == 'application/x-www-form-urlencoded':
      body=ast.literal_eval(Handle.get_argument('body'))
      #print(type(body))
      try:
         _key=body['MT'][0]["Evt"]
         _evt=CEvt[ _key ]
         val=body['MT'][0][_key][0]
         #log.info(f"EV={_evt} key={_key} rec={len(val)}")
         __Serialize( _key,body )
         _isExit=Process.MatrixJsonPostHandler( Handle,_evt,body )
      except KeyError:
         log.error(" Key Error " )
      except Exception as e: # origin Exception
         log.error(f'::origin Exception Error by MatrixJsonPostHandler {e} ty:{type(e)} {e} ')
   
   if( _isExit ):
        len_body=0
   else:
      if(type(body) == CEvt ):
         len_body=len(type(body))
      else:
         len_body=len(body)
         #log.info(body)
         #log.info(type(body))
   #log.error(" MatrixJsonPostHandler END !!!!!" )
   return(len_body)

def __Serialize( key,dic):
   pass
   """
   import general.utility.pickler as pp
   #if( key == CEvt.ESTI.name ):
   if( key == CEvt.TRAN.name ):
      #pass
      f=pp.gwtUniqueFileNamee(".pickle")
      pp.Serialize(f,dic)
   """