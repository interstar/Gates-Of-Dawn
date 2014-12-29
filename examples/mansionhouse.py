from god import *
from basic_monosynth import basic_synth, twin_osc

def noise_fm(id) :
    return fm(mult_(noise_(num()),1000),id)
    
    
if __name__ == '__main__' :
    with patch("basic_synth.pd") as taken :
        outlet_ ( basic_synth(twin_osc(slider("pitch_$0",0,1000)),"$0") )
        guiCanvas()

    with patch("basic_fm.pd") as taken :
        outlet_ ( basic_synth(noise_fm(slider("pitch_$0",0,1000)),"$0") ) 
        guiCanvas()

    with patch("mansion2.pd") as taken :
        t_lfo = hslider("Melody_LFO",-10,10)
        t_ff = hslider("Melody_Filt_Freq",-10,10)
        f_lfo = hslider("FM_LFO", -10, 10)
        f_ff = hslider("FM_Filt_Freq", -10, 10) 
        
        def addt(ab) : return add_input(t_ff, add_input(t_lfo,ab,0), 1)
        def addf(ab) : return add_input(f_ff, add_input(f_lfo,ab,0), 1)
        
        dac_( addt(abstraction("basic_synth",800,50)),
              addt(abstraction("basic_synth",800,50)),
              addt(abstraction("basic_synth",800,50)),
                      
              addf(abstraction("basic_fm",800,50)),
              addf(abstraction("basic_fm",800,50)),
              addf(abstraction("basic_fm",800,50))
        )
    
  
