
from god import *
from parts import * 


def noise_fm(id) :
    return fm(sigmult(noise(num()),1000),id)
    
def basic_synth(src,id=1) :
    return vol(
        simple_delay(
            lfo(
               filtered(
                    src
               ,id)
            ,id)
        ,1000,"echo_%s"%id)
    ,id)



def twin_osc(id=1) :
    #pitch = slider("twin_pitch_%d"%id,50,1000)
    #pitch = midi_notes()
    pitch = num()
    script.connect(note(36),pitch,0)
    script.connect(note(38),pitch,0)
    script.connect(note(41),pitch,0)
    script.connect(note(43),pitch,0)
    script.connect(note(48),pitch,0)
    
    
    diff = sigadd(pitch,slider("twin_pitch_diff_%d"%id,0,20))
   
    return sigadd(
             sigadd(phasor(pitch),-0.5),
             sigadd(phasor(diff),-0.5)
           )    
    
def counterTest() :
    script.clear()
    num(counter(metronome(bang("metro counter"),"500")))
    print script.out()    

def bigSynths() :
    script.clear()
    script.cr()
    s1 = basic_synth(twin_osc(1),1)
    script.cr()
    s2 = basic_synth(twin_osc(2),2)
    script.cr()
    s3 = basic_synth(twin_osc(3),3)
    script.cr()
    s4 = basic_synth(noise_fm(4),4)
    dac(s1,s2,s3,s4)
    print script.out()
    
counterTest()

