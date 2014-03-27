from god import *
from basic_monosynth import *

def dist(src,val) :
    return clip_(src,mult_(val,-1),val)
    
if __name__ == '__main__' :
    script.clear()
    
    
    lfo = snapshot(
        add_(mult_(sin_(slider("clip lfo",0,"0.5")),0.5),0.5)
        ,metronome(script.getLoadBang(),"5")
    )
    
    dac_(vol(
        filtered(
            dist(
                sin_(slider("pitch",0,1000))
                #,num(slider("clip",0,1))
                ,num(lfo)
            )
        )        
    ,1))
    print script.out()
    
        
