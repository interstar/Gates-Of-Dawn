from god import *

def twin_osc(freq,id=1,diff=None) :
    if diff is None : diff = slider("twin_pitch_diff_%d"%id,0,20)    
    diff = sigadd(freq,diff)
    return sigadd(
             sigadd(phasor(freq),-0.5),
             sigadd(phasor(diff),-0.5)
           )    

def basic_synth(src,id=1) :
    return vol(
        simple_delay(
            lfo(
               filtered(
                    src
               ,id)
            ,id)
        ,1000,"$0_echo_%s"%id)
    ,id)
    
if __name__ == '__main__' :

    with makeFile("simpleMono.pd") as f :
        s1 = basic_synth(twin_osc(slider("pitch1"),1),1)
        sigoutlet(s1)
        guiCanvas()
        
    with makeFile("gcontainer.pd") as f :
        dac( abstraction("simpleMono",800,50), 
             abstraction("simpleMono",800,50),
             abstraction("simpleMono",800,50)
             
             )

