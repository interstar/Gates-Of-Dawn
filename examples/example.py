
from god import *

 

def dist(src,val) :
    return sigclip(src,"%s"%-val,"%s"%val)

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
    
    
               
def counterTest() :
    script.clear()
    num(cycler(metronome(bang("metro counter"),"500"),"16"))
    print script.out()    


def clippedSin() :
    script.clear()
    dac(vol(filtered(dist(sin(slider("pitch",0,1000)),0.5)),1))
    print script.out()
    
    

def simpleSynth() :

    
    #s2 = basic_synth(twin_osc(midi_notes(),2),2)
    
    
    #s1 = vol(new_env(filtered(twin_osc(midi_notes(),1),1),1),1)
    
    #s1 = vol(new_env(filtered(fm(twin_osc(midi_notes(),1),1),1),1),1)
 
    #s1 = midi_filtered(ctl_twin(1))
    
    
simpleSynth()

