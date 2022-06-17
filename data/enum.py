from enum  import Enum,IntEnum

class CSts(IntEnum):
    MiN    = -1
    #IDLE   = 0      #アイドル状態
    LOGOUT = 0
    LOGIN  = 1
    CONNECT= 2       # connecting 通信中
    MAX    = 3
    TRADING =5
    NOCHG  =98
    INSIDE =99
    NONE   =-1

class CEvt(IntEnum):
    MiN  = -1 #
    GET  = 0  #
    POST = 1  #
    ESTI = 2  #
    TRAN = 3  #
    MAX  = 4  #
    TIMER= 5  #
    NONE = 6  #
    #ESTI= 7  #
    #END  = 9
    #INIT =1
    #DB_UP=98
    TO_W =8       # Androidへ変更
    TO_A =9       # Windowsへ変更
    AMOUNT=76     # 投資額変更
    ViSUAL=77     #visualization
    SOUND=78      # 音を鳴らす
    SETLOSS=79
    RLIST=80
    MART=81       # Martingale
    SREQEEXCEL=82 # EexcelExport
    SREQCLR=83    # tradeSummaryClear
    STRNCLR=84    # tranSummary
    PREP_TH=85    # Prepare thread
    TRADE_TH=86 # Trade thread
    CON_FIN=87  # connect finish
    TO_DEMO=89 #
    TO_REAL=90 #
    REQU =91   #
    BCLOSE=92
    REFRESH=93  #
    BOPEN=94    #
    CLOSE=95    #
    OPEN =96    #
    STOP =97    #
    OTHER=98    #
    NOP  =99

#browser size small or large
class CBSize(IntEnum):
    SMALL=0
    LARGE=1

# 0b, 0o, 0x
class CFlags(IntEnum):
#class CSysFlags(IntEnum):
    CLEAN   =0x0000   #問題無し
    SUCCESS =0x0001   #処理成功
    FAILED  =0x0002   #処理失敗
    REJECT  =0x0004   #取引システム約定拒否状態
    B_DOWN  =0x0008   #ブラウザと接続できていない
    B_SIZ   =0x0010   #ブラウザがラージサイズで表示れている
    B_OPEN  =0x0020   #ブラウザオープン中
    B_AMERR =0x0040   #残額が残っている

# サブプロセス起動モード
class CPpsm(IntEnum):       #CSubProcessStartupMode
    SINGLE=0
    THREAD=1
    PROCESS=2

#　webdriver 起動オプション
class CPmd(IntEnum):       #CPlatformMode
    NOCHG=0     #設定そのまま使う
    NOSTART=1   #起動しない
    TO_W =2     # Androidへ変更
    TO_A =3     # Windowsへ変更

class CEsti(IntEnum):       # Estimate
    PASS=0          
    Buy =1
    Sell=2
    RBuy =3
    RSell=4
    Win=3
    Lose=4
    #OofR=3        #Out of range