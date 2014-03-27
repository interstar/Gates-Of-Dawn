from god import *

def twin_osc(freq,id=1,diff=None) :
    if diff is None : diff = slider("twin_pitch_diff_%d"%id,0,20)    
    diff = add_(freq,diff)
    return add_(
             add_(phasor_(freq),-0.5),
             add_(phasor_(diff),-0.5)
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
    with makeFile("basic_monosynth.pd") as f :
        s1 = basic_synth(twin_osc(slider("pitch1"),1),1)
        dac_(s1)

