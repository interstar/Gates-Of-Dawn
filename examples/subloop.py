from god import *
from basic_monosynth import twin_osc, basic_synth

# A demo sequencer that plays two mono-synths. Each monosynth has adjustable amplitude and filter AD envelopes
# Plays the Sublime Loop :-) http://www.sublimeloop.com/


def env_filtered(sig,trigger,id=1) :
    """ Envelope controls filter """
    return vcf_(sig,
               triggered_env(num(msg(script.getLoadBang(),1000)),trigger,"env_freq_%s"%id),
               #triggered_env(num(msg(script.getLoadBang(),10)),trigger,"env_res_%s"%id)
               slider("filter_env_res%s"%id,0,10)
           )

def sequence(trigger,*vals) :
    """
    Simple sequence
    """
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

if __name__ == '__main__' :
    # A pair of monosynths controlled by a step sequencer
    
    with patch("triggered_synth.pd") as f :
        met = inlet()
        pitch = inlet()
        
        syn = vol(simple_delay(
            triggered_env(
                  env_filtered(
                      twin_osc(pitch,"$0"),
                  met,"$0"),
              met, "$0")
           ,5000,"echo$0"),"$0")
        outlet_(syn)
        vNum(pitch)
        guiCanvas()
               
    
    with patch("met.pd") as f :
        outlet( metronome(bang("metro"),"500") )
        guiCanvas()


    with patch("seq.pd") as f :
        met = abstraction("met",400,50)
        
        cyc = cycler(met,"16")
        vNum(cyc)
        
        seq  = sequence(cyc,48,51,48,51, 50,53,50,53, 46,50,46,50, 48,52,48,52)  
        seq2 = sequence(cyc,32,32,32,32, 34,34,34,34, 31,31,31,31, 28,28,28,28)
        
        vNum(seq)
        vNum(seq2)

        syn1 = abstraction("triggered_synth",800,50,sources=[seq,met])
        syn2 = abstraction("triggered_synth",800,50,sources=[seq2,met])                  
                      
        dac_(syn1,syn2)

