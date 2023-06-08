import os
import os.path as path
from datetime import datetime
import tornado.ioloop
from concurrent.futures import ProcessPoolExecutor
import winsound
from data.enum import CEvt
from data.environment.LivingFieldEnv.Folder import GrFolderDict as fenv
from general.utility.logger import log
import general.utility.pickler as pp
from general.utility.Requester import doCreate

class CSoundHandler():

    #メンバー変数
    __FOLDER__=path.join(fenv['data'],'Sounds')

    @classmethod
    def PlaySound(cls,fileName ):
        try:
            _key=CEvt.SOUND.name
            f=os.path.join(fenv['Request'],pp.gwtUniqueFileNamee(".pickle"))
            dic=doCreate( _key,fileName )
            pp.Serialize(f,dic)
        except Exception as e: # origin Exception
            log.error( f'{__name__} CSoundHandler::PlaySound Exception  catch!! t:{type(e)} fileName:{ fileName } e={e}')
            pass

    @classmethod
    def PlaySound2(cls,fileName ):
        try:
            #print("aaaaaaa")
            _File_PATH=path.join(cls.__FOLDER__,fileName)
            ioloop = tornado.ioloop.IOLoop.current()
            #print(f"::CSoundHandler 音をならします1 F:{_File_PATH} {datetime.now()} !!!!!! ")
            #音を別プロセスで起動する(クラスのインスタンスは渡せない)
            ioloop.current().run_in_executor( ProcessPoolExecutor(),cls._PlaySound,_File_PATH )
            #ioloop.run_in_executor( None,cls._PlaySound,_File_PATH )
        except Exception as e: # origin Exception
            log.error( f'{__name__} CSoundHandler::PlaySound2 Exception  catch!! t:{type(e)} fileName:{ fileName } e={e}')
            pass

    def _PlaySound(File_PATH):
        #print(f"::CSoundHandler 音をならします2 F:{File_PATH} {datetime.now()} !!!!!! ")
        if(os.path.isfile(File_PATH)):
            #音がうるさいので一旦中断
            winsound.PlaySound(File_PATH, winsound.SND_FILENAME)
            pass
