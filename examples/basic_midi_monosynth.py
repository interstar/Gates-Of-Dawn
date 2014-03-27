from basic_monosynth import *

if __name__ == '__main__' :
    with makeFile("basic_midi_monosynth.pd") as f :
        s1 = basic_synth(twin_osc(midi_notes(),1),1)
        dac_(s1)

