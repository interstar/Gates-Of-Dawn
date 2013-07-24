from god import *
from basic_monosynth import basic_synth, twin_osc

def noise_fm(id) :
    return fm(sigmult(noise(num()),1000),id)
    
if __name__ == '__main__' :
    script.clear()
    script.cr()
    s1 = basic_synth(twin_osc(slider(1)),1)
    script.cr()
    s2 = basic_synth(twin_osc(slider(1)),2)
    script.cr()
    s3 = basic_synth(twin_osc(midi_notes()),3)
    script.cr()
    s4 = basic_synth(noise_fm(slider(1)),4)
    dac(s1,s2,s3,s4)
    print script.out()
    
   
