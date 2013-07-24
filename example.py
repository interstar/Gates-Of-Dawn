
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

def some_notes() :
    pitch = num()
    script.connect(note(36),pitch,0)
    script.connect(note(38),pitch,0)
    script.connect(note(41),pitch,0)
    script.connect(note(43),pitch,0)
    script.connect(note(48),pitch,0)
    return pitch
    
def twin_osc(freq,id=1) :   
    diff = sigadd(freq,slider("twin_pitch_diff_%d"%id,0,20))
   
    return sigadd(
             sigadd(phasor(freq),-0.5),
             sigadd(phasor(diff),-0.5)
           )    

def ctl_twin(id) :
    m = midi_notes()
    diff = sigadd(m,slider(id,0,20))
   
    return sigadd(
             sigadd(phasor(m),-0.5),
             sigadd(phasor(diff),-0.5)
           )    
    
    
def env_filtered(sig,trigger,id=1) :
    return vcf(sig,
               triggered_env(num(msg(script.getLoadBang(),1000)),trigger,"env_freq_%s"%id),
               #triggered_env(num(msg(script.getLoadBang(),10)),trigger,"env_res_%s"%id)
               slider("filter_env_res%s"%id,0,10)
           )
               
def counterTest() :
    script.clear()
    num(cycler(metronome(bang("metro counter"),"500"),"16"))
    print script.out()    

def bigSynths() :
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
        script.connect(msg(script.getLoadBang(),v),fb,1)
        
        #script.connect(slider("slider_%s"%i,0,128,default=32),fb,1)
        script.connectFrom(s,i,fb,0)
        script.connect(fb,freq,0)
        i=i+1
    return freq
    
def seqSin() :
    # A synth controlled by a step sequencer, with a second synth controlled by midi
    script.clear()
    
    met = metronome(bang("metro"),"400")
    cyc = cycler(met,"16")
    # quick Sublime Loop :-) http://www.sublimeloop.com/
    seq = sequence(cyc,48,51,48,51, 50,53,50,53, 46,50,46,50, 48,52,48,52)
    num(seq)
    script.cr()
    syn1 = triggered_env(
                env_filtered(twin_osc(seq,1),met,1),
                met
            ,1)
    syn2 = triggered_env(
                env_filtered(twin_osc(midi_notes(),2),met,2),
                met
            ,2)
          
    dac(vol(simple_delay(syn1,1000,"del1")),vol(simple_delay(syn2,1000,"del2")))
    print script.out()

def simpleSynth() :
    script.clear()
    script.cr()
    #s1 = basic_synth(twin_osc(slider("pitch1"),1),1)
    
    s1 = basic_synth(twin_osc(midi_notes(),1),1)
    
    #s2 = basic_synth(twin_osc(midi_notes(),2),2)
    
    
    #s1 = vol(new_env(filtered(twin_osc(midi_notes(),1),1),1),1)
    
    #s1 = vol(new_env(filtered(fm(twin_osc(midi_notes(),1),1),1),1),1)
 
    #s1 = midi_filtered(ctl_twin(1))
    dac(s1)
    print script.out()
    
simpleSynth()
#bigSynths()
