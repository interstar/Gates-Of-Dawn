from god import *


def twin_osc(freq,id=1,diff=None) :
    if diff is None : diff = slider("$0_twin_pitch_diff_%s"%id,0,20)    
    diff = add_(freq,diff)
    return add_(
             add_(phasor_(freq),-0.5),
             add_(phasor_(diff),-0.5)
           )    


def lessfiltered(sig,id=1) :
    i = add_input(inlet(),slider("cutoff_%s",0,1000))
    return vcf_(sig,
               vNum(i),
               #mult_(phasor_(add_input(inlet(),slider("filt_freq_phasor_speed_%s"%id,-10,10,default=0.0001))),1000),
               num(slider("filter_res_%s"%id,0,10))
           )


def synth(src,trigger,id=1) :
    return vol(
        simple_delay( 
            triggered_env(
                lessfiltered(src,id)
               ,trigger,id)             
        ,1000,"$0_echo_%s"%id)
    ,id)



with patch("hello.pd") as f :
    b = bang("note on")
    s = select(inlet(),"1")
    script.connectFrom(s,0,b,0)
    outlet_ ( synth(twin_osc( vNum(inlet()),"$0"),b,"$0") )
    guiCanvas()


def make_synth(osc_in,no,noIns) :
    router = osc_routed(osc_in,"/channel%s"%no,noIns)
    ab = abstraction("hello",800,50)
    script.connectFrom(router,0,ab,2)
    script.connectFrom(router,1,ab,1)
    script.connectFrom(router,2,ab,0)
    script.connectFrom(router,3,ab,3)
    return ab
    
def mix(*sigs) :
    m = add_(sigs[0],0)
    for s in sigs[1:] :
        script.connect(s,m,0)
    return vol(m)
    
with patch("hello_main.pd") as f :    
    importer("mrpeach")

    oin = osc_in(9004)
    
    
    dac_( mix(
        make_synth(oin,0,4),
        make_synth(oin,1,4),
        make_synth(oin,2,4),
        make_synth(oin,3,4), 
        make_synth(oin,4,4),
        make_synth(oin,5,4)
    ) )
    
