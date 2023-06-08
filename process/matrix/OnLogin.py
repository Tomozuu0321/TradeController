from general.utility.logger import MatrixFunction,log
from general.utility.StopWatch import MatrixFunctionEx
from data.enum import CEvt
from data.environment.LivingFieldEnv.BrowserEnv import BrEmv

#@MatrixFunction
def OnLogin(Params,sts,evt):

    if( Params.Mode() != BrEmv.ModeDemo ):
        OnLoginR(Params,sts,evt)
    else:
        OnLoginD(Params,sts,evt)

#@MatrixFunction
@MatrixFunctionEx
def OnLoginD(Params,sts,evt):
    if( evt==CEvt.TO_DEMO ):
        __ModeChange( Params,sts,evt,BrEmv.ModeDemo)

    from process.matrix.modules.biWinning.__DemoLogin import _login
    _login(Params,Params.driver)

@MatrixFunction
def OnLoginR(Params,sts,evt):
    if( evt==CEvt.TO_REAL ):
        __ModeChange( Params,sts,evt,BrEmv.ModeReal)

    from process.matrix.modules.biWinning.__RealLogin import _login
    _login(Params,Params.driver)

def __ModeChange(Params,sts,evt,mode ):
    from process.matrix.OnOpen  import OnOpen
    from general.data.informationSystem import CinformationSystem
    info=CinformationSystem()
    info.to_sql(Params.Mode(),Params.dfs)
    Params.Mode(mode)
    OnOpen(Params,sts,evt)
    Params.Mode(mode)
    info=CinformationSystem()
    info.to_sql(Params.Mode(),Params.dfs)

