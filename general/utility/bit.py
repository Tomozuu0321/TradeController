# bit操作
def Chk( inpTarget,inpChkBits ):
    return((inpTarget)&(inpChkBits));
def Set( inpTarget,inpChkBits ):
    return((inpTarget)|(inpChkBits));
def Clr( inpTarget,inpChkBits ):
    return((inpTarget)&(~inpChkBits));
def Chg( inpTarget,inpChkBits ):
    return((inpTarget)^(inpChkBits));
