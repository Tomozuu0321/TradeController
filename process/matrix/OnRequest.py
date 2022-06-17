# %%
import os
from data.enum import CEvt
from general.utility.logger import MatrixFunction,log
from data.environment.LivingFieldEnv.Folder import GrFolderDict as fenv
import general.utility.pickler as pp
from general.utility.Requester import doCreate,doRequest
from concurrent.futures import ProcessPoolExecutor
@MatrixFunction
def OnRequest2(Params,sts,evt):

    _c=type(Params.Receive)
    if _c != CEvt :
        return
    _key=Params.Receive.name;
    

    #doRequest( _key,"this Test Request")
    with ProcessPoolExecutor(max_workers=1) as Executor:
        future1=Executor.submit(doRequest, _key,"this Test Request",Params.GetUrlEx(0,0,1))

@MatrixFunction
def OnRequest1(Params,sts,evt):

    #
    # 上手く送信ができないので一旦ピクル化して以後に託す
    #
    _c=type(Params.Receive)
    if _c != CEvt :
        return
    _key=Params.Receive.name;
    f=os.path.join(fenv['Request'],pp.gwtUniqueFileNamee(".pickle"))
    dic=doCreate( _key,"this Test Request")
    pp.Serialize(f,dic)
