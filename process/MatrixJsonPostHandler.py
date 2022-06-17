import os
import glob
import pickle
import urllib
import json

from data.enum import CSts,CEvt
from data.environment.LivingFieldEnv.Folder import GrFolderDict as fenv
from general.utility.logger import log
import general.utility.pickler as pp
#import tornado.ioloop
#import tornado.web
#import tornado.ioloop

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

# %%
def MatrixJsonPostHandler(Handle,Process):

   self=Handle
   #log.info(self.head)
   #log.info(type(self.head))
   #log.info(self.request.headers.get('Content-Type'))

   _isExit=False
   #if self.request.headers.get('Content-Type') == 'application/x-www-form-urlencoded':
   if self.request.headers.get('Content-Type') == 'application/json':
      byte=urllib.parse.unquote_to_bytes(json.loads(self.request.body.decode('utf-8')))
      body=pickle.loads(byte)
      try:
         _key=body['MT'][0]["Evt"]
         _evt=CEvt[ _key ]
         val=body['MT'][0][_key][0]
         log.info(f"EV={_evt} key={_key} rec={len(val)}")
         #debug 
         __Serialize( _key,body )
         _isExit=Process.MatrixJsonPostHandler( Handle,_evt,body )

      except KeyError:
         log.error(" Key Error " )

   if( _isExit ):
        len_body=0
   else:
      if(type(body) == CEvt ):
         len_body=len(type(body))
      else:
         len_body=len(body)
         #log.info(body)
         #log.info(type(body))

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