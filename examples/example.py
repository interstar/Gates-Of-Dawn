
from god import *
 


def some_notes() :
    pitch = num()
    script.connect(note(36),pitch,0)
    script.connect(note(38),pitch,0)
    script.connect(note(41),pitch,0)
    script.connect(note(43),pitch,0)
    script.connect(note(48),pitch,0)
    return pitch
    


def ctl_twin(id) :
    m = midi_notes()
    diff = sigadd(m,slider(id,0,20))
   
    return sigadd(
             sigadd(phasor(m),-0.5),
             sigadd(phasor(diff),-0.5)
           )    
    
    




