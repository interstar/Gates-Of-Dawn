from god import *
from basic_monosynth import twin_osc

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
    # A synth controlled by a step sequencer, with a second synth controlled by midi
    with patch("seq.pd") as f :
    
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
              
        dac_(vol(simple_delay(syn1,5000,"echo")))

