from god import *
from basic_monosynth import basic_synth, twin_osc

def noise_fm(id) :
    return fm(mult_(noise_(num()),1000),id)
    
    
if __name__ == '__main__' :
    with patch("basic_synth.pd") as taken :
        outlet_ ( basic_synth(twin_osc(slider("pitch_$0",0,1000)),1) )
        guiCanvas()

    with patch("basic_fm.pd") as taken :
        outlet_ ( basic_synth(noise_fm(slider("pitch_$0",0,1000)),4) ) 
        guiCanvas()

    with patch("mansion2.pd") as taken :
        dac_( abstraction("basic_synth",800,50), 
              abstraction("basic_synth",800,50), 
              abstraction("basic_synth",800,50), 
              abstraction("basic_fm",800,50), 
              abstraction("basic_fm",800,50),
              abstraction("basic_fm",800,50) 
        )
    
   
