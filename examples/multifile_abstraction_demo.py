from god import *

# Demonstrates how to make two files :
# one containing a simpleMono synth, 
# and a second which includes it as a PD "Abstraction" a couple of times.

from basic_monosynth import twin_osc, basic_synth
    
if __name__ == '__main__' :

    with patch("simpleMono.pd") as f :
        s1 = basic_synth(twin_osc(slider("pitch1"),1),1)
        outlet_(s1)
        guiCanvas()
        
    with patch("gcontainer.pd") as f :
        dac_( abstraction("simpleMono",800,50), 
              abstraction("simpleMono",800,50),
              abstraction("simpleMono",800,50)             
        )

