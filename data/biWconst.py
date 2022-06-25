from dataclasses import dataclass

@dataclass(frozen=True)
class CbiWconst:

#print(" CbiWconst init Call")

    #from general.data.environment.LivingFieldEnvUrl import CLivingFieldEnvUrl as U
    #HOME:str= Params.GetUrl(1)  #(U().doRead()['Url'][1])
    Home="https://www.bi-winning.org"
    Top:str="/#"
    Tranding:str=Home+"/trading#/"
    Min:int=1010            # 大画面　小画面のしきい値
    Amount:int=500          # 投資額ベース
    TargetCurrency:str="ビットコイン"
    #TargetCurrency:str="Ethereum"
    CurrencyIndex:int=1     # あやしまれるかもしれんのでイーサ
    #CurrencyIndex:int=2     # あやしまれるかもしれんのでイーサ
    lossCutBase:float=10.0
    Sleep:int=1
    #print(HOME)
    MaxValune=3000
    #MaxValune=5000          
    LoginKey0:str="投資額"
    LoginKey1:str="残高"
    InvalidValue:float=-1000000.987654321
    RejectWord:str="取引を実行できません"       # この銘柄は高ボラティリティのため、現在取引を実行できません。再試行してください
    SuccessWord:str="取引は正常に開かれました"  # "取引は正常に開かれました" 
    NoticeSound:str="onepoint17.wav"          # "chime03.wav"
    NoticeModeSound:str="chime03.wav"
    lossCutSound:str="jingle03.wav"
    lossUpdateSound=str="chime04.wav"
    Dig:int=3                                  # floatDigit 少数点の表示桁数
    coefficient:float=1.23                     # ２回目以降のPAYOUTがイーブンになるための倍率

const=CbiWconst()
#print(" CbiWconst init END")