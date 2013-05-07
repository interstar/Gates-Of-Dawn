
from god import script, dac, sin, mult, sigmult, add, sigadd, sub, sigsub, phasor, noise, num, vcf, slider, mtof, sigmtof, note_in, ctl_in

def fm(sig,id=1) :
    return sin(sigadd(
                sig,
                sigmult(
                   phasor(num(slider("fm_freq_%s"%id,-1000,1000))),
                   num(slider("fm_amp_%s"%id,-500,500))
                )
           ))
        
def vol(sig,id=1) :
    return sigmult(sig,num(slider("vol_%s" % id,0,1)))
  
def filtered(sig,id=1) :
    return vcf(sig,
               num(slider("filter_freq_%s"%id,0,1000)),
               num(slider("filter_res_%s"%id,0,10))
           )


def fm_noise(id=1) :
    return vol(
        sigmult(
            filtered(
                fm(sigmult(noise(num()),1000),id)
            ,id),
            phasor(num(slider("lfo_%s"%id,-40,40)))
        )    
    ,id)

def midi_filtered(sig,id=1) :
    # Gets filter frequency from MIDI control (basic experiment, only the default channel info so far)
    return vcf(sig,
               mult(ctl_in(),10),
               num(slider("filter_res_%s"%id,0,10))
           )



def fm_synth(id=1) :
    # Gets note and filter frequency via MIDI (basic experiment, no channel selection yet)
    return vol(
        sigmult(
            midi_filtered(
                fm(sigmult(sin(num(mtof(note_in()))),1000),id)
            ,id),
            phasor(num(slider("lfo_%s"%id,-40,40)))
        )    
    ,id)


def lfo(sig,id=1) :
    return sigmult(
        sig,
        phasor(slider("lfo_%s"%id,-40,40))
    )

def twin_osc(id=1) :
    pitch = slider("twin_pitch_%d"%id,50,1000)
    diff = sigadd(pitch,slider("twin_pitch_diff_%d"%id,0,20))
    
    return vol(filtered(lfo(
        sigadd(
            sigadd(phasor(pitch),-0.5),
            sigadd(phasor(diff),-0.5)
        )
    ,id),id),id)
    
    

script.clear()

dac(fm_noise(),fm_noise(2),fm_synth(3),twin_osc(4))

print script.out()

