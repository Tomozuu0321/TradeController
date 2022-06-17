from dataclasses import dataclass
from data.enum import CPmd      #CFlags,CSts,CPmd

@dataclass(frozen=True)
class CBrowserEnv:

    def __isDebug():
        import sys
        if "debugpy" in sys.modules:
            #print('VSCodeからデバッグされてます')
            return(True)
        else:
            #print('VSCodeからデバッグされてません')
            return(False)

    PlatformWindows:str='Windows'   #
    PlatformAndroid:str='Android'   #
    ModeDemo:str='demo'             #
    ModeReal:str='Real'             #
    DefMode:str=ModeDemo            # ModeReal ModeDemo
    CookieUse:bool=True             #
    RefreshRate:int=4
    PageRefresh:int=0
    Digits:int=2                    # 浮動小数点桁数
    HttpSessionCheck:float=0.005    #
    DRefreshCountForNoteBooK:int=10 #開発用ループカウンター
    TriggerSeconds:int=25
    ShortStart:bool=False           # True DBを使わず短縮起動する
    isGgraphNotShow:bool=__isDebug()   # グラフ表示有無
    ShortStart:bool=False           # True DBを使わず短縮起動する
    #ShortStart:bool=True            # True DBを使わず短縮起動する
    JsonWrite:bool=True #False            # 終了時にSystem.jsonを更新
    PlatformMode:CPmd=CPmd.NOCHG    # webdriver 起動オプション
    #PlatformMode:CPmd=CPmd.NOSTART  #CPmd.NOCHG    # webdriver 起動オプション
    #StartSts:CSts=CSts.MiN         # 今は設定よめればOKなので不要
    visualization:int=1             # 0:ファイル出力 1:画面出力
    LoadtTimeout:int=10             #
    ImplicitlyWwait:int=10          # driver.implicitly_wait(time_to_wait
    DefAction:str="Trading"
    WaitAction:str="Waiting"
    SummaryIndex0:str="Daily"
    SummaryIndex1:str="Accum"
    visualFile:str='chart1010.png'
    visualPAth:str='./static/image/'

BrEmv=CBrowserEnv()
    