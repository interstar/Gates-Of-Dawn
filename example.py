
from god import script, dac, sin, mult, sigmult, add, sigadd, sub, sigsub, phasor, noise, num
from god import vcf, slider, mtof, sigmtof, note_in, ctl_in, simple_delay, msg, vline, bang, pack, a_float



        
def vol(sig,id=1) :
    return sigmult(sig,num(slider("vol_%s" % id,0,1)))

def lfo(sig,id=1) :
    return sigmult(
        sig,
        phasor(slider("lfo_%s"%id,-15,15))
    )


def fm(sig,id=1) :
    return sin(sigadd(
                sig,
                sigmult(
                   phasor(num(slider("fm_freq_%s"%id,-1000,1000))),
                   num(slider("fm_amp_%s"%id,-500,500))
                )
           ))
  
def filtered(sig,id=1) :
    return vcf(sig,
               sigmult(phasor(slider("filt_freq_phasor_speed_%s"%id,-10,10)),1000),
               #num(slider("filter_freq_%s"%id,0,1000)),
               num(slider("filter_res_%s"%id,0,10))
           )


def midi_filtered(sig,id=1) :
    # Gets filter frequency from MIDI control (basic experiment, only the default channel info so far)
    return vcf(sig,
               mult(ctl_in(),10),
               num(slider("filter_res_%s"%id,0,10))
           )

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
    
def midi_notes() :
    return mtof(note_in())

def note(n) :
    return mtof(msg(n))
    
def envelope(sig,id) :
    m = msg("1 10 \, 1 100 2000 \, 0 100 1000")
    b = bang("envelope_%s" % id)
    script.connect(b,m,0)
    return sigmult(
        sig,
        vline(m)
    )

def new_env(sig,id) :
    b = bang("envelope_%s" % id)
    attack = num(slider("attack_%s"%id,0,100))
    script.connect(b,attack,0)
    decay = num(slider("decay_%s"%id,0,10000))
    p = pack(attack,"f","f")
    script.connect(decay,p,1)
    return sigmult(
        sig,
        vline(msg(p,"1 \$1 \, 0 \$2 \$1"))
    )
    
    

script.clear()

#dac(vol(filtered(phasor(num(slider("slide1",0,1000))))))

s1 = basic_synth(twin_osc(1),1)
script.cr()
s2 = basic_synth(twin_osc(2),2)
script.cr()
s3 = basic_synth(twin_osc(3),3)
script.cr()
s4 = basic_synth(noise_fm(4),4)
dac(s1,s2,s3,s4)

print script.out()

