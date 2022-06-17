#"""
from os import path
#import os.path as path
import pandas as pd
import json #必ず必要
from data.environment.LivingFieldEnv.Folder import GrFolderDict as fenv

#"""

class CLivingFieldEnvAccount():

    #メンバー変数
    _folder=path.join( path.join(fenv['data'],'environment'),'LivingFieldEnv')
    _jsonPath=path.join( _folder,'Account.json')
    _excel_path=path.join( _folder,'Account.xlsx')
    #_df=None
    
    #print(os.getcwd())
    #辞書オブジェクト雛形作成
    def doCreate(self):
        _dic = dict(
        {
            "id":"jks01knr@gmail.com",
            "password":"6UCVmhsD83"
        })
      
        return(_dic)

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
        _df=pd.read_excel(self._excel_path)
        print(_df)

        _dic={0:"0"}
        _dic.clear()

        for i in range(len(_df)):
            for j in range(len(_df.columns)):
                #
                # 辞書[キー] = 値
                # columnsはindexなのでスキップする
                if( j !=0 ):
                    #print( "%d,%s" % ( j,type(j)))
                    #print('{0},{1}'.format(j,type(j)))
                    _dic[_df.columns[j]] = _df[_df.columns[j]][0]

        return(_dic)

    #クセルファイル書き込み
    def to_excel(self,dic):
        #
        #Python 辞書を Pandas DataFrame に変換する方法
        #
        #_df=pd.DataFrame.from_dict(dict,orient='index')
        # #_df=pd.DataFrame.from_dict(dict,orient='list')
        _df= pd.DataFrame(dic,index=['i',])
        _df.to_excel(self._excel_path)

