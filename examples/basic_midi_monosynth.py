from basic_monosynth import *

if __name__ == '__main__' :
    with patch("basic_midi_monosynth.pd") as f :
        s1 = basic_synth(twin_osc(midi_notes(),"$0"),"$0")
        dac_(s1)

