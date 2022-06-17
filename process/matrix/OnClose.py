from general.utility.logger import MatrixFunction,log
from general.utility.StopWatch import MatrixFunctionEx

@MatrixFunctionEx
def OnClose(Params,sts,evt):

    __InfoSysUpdate(Params,sts,evt)

    import process.matrix.modules.BrowserControl.BrowserControls as ctl
    ctl.BrClose(Params,sts,evt)

def __InfoSysUpdate(Params,sts,evt):

    from data.environment.LivingFieldEnv.BrowserEnv import BrEmv
    from general.data.informationSystem import CinformationSystem
    info=CinformationSystem()

    #if( BrEmv.ShortStart == False ):
    info.to_sql(Params.Mode(),Params.dfs)
    if( BrEmv.JsonWrite ):
        info.doWrite(Params.dfs)