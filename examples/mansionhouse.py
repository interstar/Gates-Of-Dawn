from god import *
from basic_monosynth import basic_synth, twin_osc

def noise_fm(id) :
    return fm(mult_(noise_(num()),1000),id)
    
    
if __name__ == '__main__' :
    script.clear()
    script.cr()
    s1 = basic_synth(twin_osc(slider("pitch1")),1)
    script.cr()
    s2 = basic_synth(twin_osc(slider("pitch2")),2)
    script.cr()
    s3 = basic_synth(twin_osc(slider("pitch3")),3)
    script.cr()
    s4 = basic_synth(noise_fm(slider("pitch4fm")),4)
    script.cr()
    s5 = basic_synth(noise_fm(slider("pitch5fm")),5)
    
    dac_(s1,s2,s3,s4,s5)
    print script.out()
    
   
