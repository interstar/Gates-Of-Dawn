from basic_monosynth import *

if __name__ == '__main__' :
    script.clear()
    script.cr()    
    s1 = basic_synth(twin_osc(midi_notes(),1),1)
    dac(s1)
    print script.out()
