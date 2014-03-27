from god import *

slider = hslider
        
def vol(sig,id=1) :
    return mult_(sig,num(slider("vol_%s" % id,0,1)))

def lfo(sig,id=1) :
    return mult_(sig,phasor_(slider("lfo_%s"%id,-15,15,default=0.0001)))


def fm(freq,id=1) :
    return sin_(add_(
                freq,
                mult_(
                   phasor_(num(slider("fm_freq_%s"%id,-1000,1000))),
                   num(slider("fm_amp_%s"%id,-500,500))
                )
           ))
  
def filtered(sig,id=1) :
    return vcf_(sig,
               mult_(phasor_(slider("filt_freq_phasor_speed_%s"%id,-10,10)),1000),               
               num(slider("filter_res_%s"%id,0,10))
           )


def midi_filtered(sig,id=1) :
    # Gets filter frequency from MIDI control (basic experiment, only the default channel info so far)
    return vcf_(sig,
               mult(ctl_in(),10),
               num(slider("filter_res_%s"%id,0,10))
           )

def simple_delay(sig,max_delay,name) :
    write = delaywrite_(sig,max_delay+1,name)
    read = delayread_(slider("%s_feedback_time"%name,0,max_delay),name)
    fback = mult_(read,slider("%s_feedback_gain"%name,0,0.9))
    script.connect(fback,write,0)
    return read
    
def midi_notes() :
    return mtof(note_in())

def note(n) :
    return mtof(msg(n))
    
def envelope(sig,id) :
    m = msg("1 10 \, 1 100 2000 \, 0 100 1000")
    b = bang("envelope_%s" % id)
    script.connect(b,m,0)
    return mult_(
        sig,
        vline_(m)
    )



def new_env(sig,id) :
    b = bang("envelope_%s" % id)
    attack = num(slider("attack_%s"%id,0,100))
    script.connect(b,attack,0)
    decay = num(slider("decay_%s"%id,0,10000))
    p = pack(attack,"f","f")
    script.connect(decay,p,1)
    return mult_(
        sig,
        vline_(msg(p,"1 \$1 \, 0 \$2 \$1"))
    )

def triggered_env(sig,trigger,id) :    
    attack = num(slider("attack_%s"%id,0,100))    
    decay = num(slider("decay_%s"%id,0,10000))
    p = pack(attack,"f","f")
    script.connect(decay,p,1)
    script.connect(trigger,attack,0)
    return mult_(
        sig,
        vline_(msg(p,"1 \$1 \, 0 \$2 \$1"))
    )
    
    

def counter(bangIn) :
    o = Generic1("int").__call__(bangIn)
    inc = add(o,1)
    script.connect(inc,o,1)
    return o
    
def metronome(start,speed) :
    met = Generic1("metro").__call__(start,speed)
    stop = msg("stop")
    script.connect(stop,met,0)
    return met
    
def cycler(metro,maxi) :
    return mod(counter(metro),maxi)
