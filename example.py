
from god import script, dac, sin, mult, sigmult, add, sigadd, sub, sigsub, phasor, noise, num
from god import vcf, slider, mtof, sigmtof, note_in, ctl_in, simple_delay

        
def vol(sig,id=1) :
    return sigmult(sig,num(slider("vol_%s" % id,0,1)))

def lfo(sig,id=1) :
    return sigmult(
        sig,
        phasor(slider("lfo_%s"%id,-40,40))
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
               num(slider("filter_freq_%s"%id,0,1000)),
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
    pitch = slider("twin_pitch_%d"%id,50,1000)
    diff = sigadd(pitch,slider("twin_pitch_diff_%d"%id,0,20))
   
    return sigadd(
             sigadd(phasor(pitch),-0.5),
             sigadd(phasor(diff),-0.5)
           )    
    
def midi_notes() :
    return mtof(note_in())
    
    

script.clear()
s1 = basic_synth(noise_fm(1),1)
script.ui_layout.cr()
s2 = basic_synth(noise_fm(2),2)
script.ui_layout.cr()
s3 = basic_synth(phasor(num(slider("synth_3_pitch",40,1000))),3)
script.ui_layout.cr()
s4 = basic_synth(twin_osc(4),4)

dac(s1,s2,s3,s4)

print script.out()

