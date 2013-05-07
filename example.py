
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
                fm(sigmult(noise(num()),1000))
            ,id),
            phasor(num(slider("lfo_%s"%id,-40,40)))
        )    
    ,id)

def midi_filtered(sig,id=1) :
    return vcf(sig,
               mult(ctl_in(),10),
               num(slider("filter_res_%s"%id,0,10))
           )



def fm_synth(id=1) :
    # Gets note and filter frequency via MIDI
    return vol(
        sigmult(
            midi_filtered(
                fm(sigmult(sin(num(mtof(note_in()))),1000))
            ,id),
            phasor(num(slider("lfo_%s"%id,-40,40)))
        )    
    ,id)


script.clear()

dac(fm_noise(),fm_noise(2),fm_synth(3))

print script.out()

