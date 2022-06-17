#"""
from os import path
#import os.path as path
import json #必ず必要
#from pandas import DataFrame
from data.environment.LivingFieldEnv.Folder import GrFolderDict as fenv
#"""

class CLivingFieldEnvUrl():

    #メンバー変数
    _folder=path.join( path.join(fenv['data'],'environment'),'LivingFieldEnv')
    _jsonPath=path.join( _folder,'Url.json')
    _excel_path=path.join( _folder,'url.xlsx')
    #_excel_path2=path.join( _folder,'url2.xlsx')

    #print(os.getcwd())

    #辞書雛形作成
    def doCreate(self):
        df = dict({
            'Url'  :['http://%s:%s/wd/hub','https://bi-winning.org/trading#/',''],
            'Host' :['localhost','192.168.1.10','Ax2010'],
            'Port' :['4444','8888','4723']
        })
        return(df)

    #josnファイル読み込み
    def doRead(self):
        #data = open('sample.json'‘読み込む JSON ファイルのパス’ , ‘r’) #ここが(1)
        fp = open(self._jsonPath,'r') #ここが(1)
        _dic= json.load(fp) #ここが(2)
        return(_dic)

    #josnファイル書き込み
    def doWrite(self,dic):
        with open(self._jsonPath, 'w') as fp:
            json.dump(dic, fp, indent=4, ensure_ascii=False)

    #エクセルファイル読み込み
    def read_excel(self):
        import pandas as pd
        _df=pd.read_excel(self._excel_path)
        _dic=_df.to_dict()
        return(_dic)

    #エクセルファイル書き込み
    def to_excel(self,dic):
        import pandas as pd
        _df = pd.DataFrame.from_dict(dic, orient='index').T
        #print(_df)
        #_df= pd.DataFrame(dic,index=['i',])
        _df.to_excel(self._excel_path,index=False)

"""
if __name__ == '__main__':

    import os
    print(os.getcwd())

    os.chdir( fenv['home'])

    print(os.getcwd())

    app=CLivingFieldEnvUrl()
    #dic=app.doCreate()
    dic=app.doRead()
    df=app.read_excel()
    print(dic)
    print(type(dic))
    #print(dic['Url']['0'])
    #app.doWrite(dic)
    #app.to_excel(dic)
"""