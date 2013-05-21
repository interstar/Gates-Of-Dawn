
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

def dist(src,val) :
    return sigclip(src,"%s"%-val,"%s"%val)


def twin_osc(id=1,pitch=None) :
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
    num(cycler(metronome(bang("metro counter"),"500"),"16"))
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

def clippedSin() :
    script.clear()
    dac(vol(filtered(dist(sin(slider("pitch",0,1000)),0.5)),1))
    print script.out()
    
def sequence(trigger,*vals) :
    nums = range(len(vals))
    def f(*args) : return Generic0("f").__call__(*args)
    def slct(*args) : return Generic1("select").__call__(*args)
    freq = Generic0("mtof").__call__()
    
    s = slct(trigger," ".join(["%s"%v for v in nums]))
    i = 0
    for v in vals :
        fb = f()
        #script.connect(msg(script.getLoadBang(),v),fb,1)
        script.connect(slider("slider_%s"%i,0,128,default=32),fb,1)
        script.connectFrom(s,i,fb,0)
        script.connect(fb,freq,0)
        i=i+1
    return freq
    
def seqSin() :
    script.clear()
    met = metronome(bang("metro"),"800")
    cyc = cycler(met,"8")
    seq = sequence(cyc,61,62,63,64,65,66,67,99)
    num(seq)
    dac(vol(triggered_env(
        filtered(fm(seq,1),1),
        met
    ,1)))
    print script.out()

seqSin()
