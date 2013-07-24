from god import *
from basic_monosynth import *

def dist(src,val) :
    return sigclip(src,sigmult(val,-1),val)
    
if __name__ == '__main__' :
    script.clear()
    
    
    lfo = snapshot(
        sigadd(sigmult(sin(slider("clip lfo",0,"0.5")),0.5),0.5)
        ,metronome(script.getLoadBang(),"5")
    )
    
    dac(vol(
        filtered(
            dist(
                sin(slider("pitch",0,1000))
                #,num(slider("clip",0,1))
                ,num(lfo)
            )
        )        
    ,1))
    print script.out()
    
        
