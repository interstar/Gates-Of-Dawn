# Gates of Dawn
# Python library to generate PureData files
# Copyright Phil Jones 2013. Released under GPL 3.0

from core import *


class Num(Unit) :

    def outPort(self) : return 0
    
    def __call__(self,*args) :        
        script.add("#X floatatom %s %s 5 0 0 0 - - -;" % (self.x,self.y))
        if len(args) > 0 :
            source = args[0]
            script.connect(source,self,0)
        
        return self

def num(*args) : return Num().__call__(*args)          

class Message(Unit) :
    """Not UI Message """
    def width(self) : return 80
    def height(self) : return 40
    def outPort(self) : return 0
    
    def __call__(self,x,y=None) :
        if y :
            script.add("#X msg %s %s %s;" % (self.x, self.y, y))
            script.connect(x,self,0)
        else :
            script.add("#X msg %s %s %s;" % (self.x, self.y, x))
        return self

def msg(*args) : return Message().__call__(*args)

        
class Generic1(Generic0) :
    """ A generic that expects 1 input signal """
    def __call__(self,in1,*args) :
        arg_string = " ".join(args)
        script.add("#X obj %s %s %s %s;" % (self.x, self.y, self.name, arg_string))
        script.connect(in1,self,0)
        return self

class Generic2(Generic0) :
    """ A generic that expects 2 inputs that are either normal or signal """
    def __call__(self,in1,in2,*args) :
        arg_string=" ".join(args)
        script.add("#X obj %s %s %s %s;" % (self.x,self.y,self.name,arg_string))
        script.connect(in1,self,0)
        script.connect(in2,self,1)
        return self

class Generic3(Generic0) :
    """ A generic that expects 3 inputs that are either normal or signal """
    def __call__(self,in1,in2,in3,*args) :
        arg_string=" ".join(args)
        script.add("#X obj %s %s %s %s;" % (self.x,self.y,self.name,arg_string))

        script.connect(in1,self,0)
        script.connect(in2,self,1)
        script.connect(in3,self,2)
        return self


class Dac(Unit) :
    def __call__(self,*args) :
        script.add("#X obj %s %s dac~;" % (self.x,self.y))
        for a in args :
            script.connect(a,self,0)
            script.connect(a,self,1)
        return self
        
def dac_(*args) : return Dac().__call__(*args)


# Operators
class Op(Unit) :
    def __init__(self,operator) :
        self.op = operator
        self._width = 60
        self._height = 40
        self.common()
        
    def outPort(self) : return 0
    
    def __call__(self,in1,in2) :
        self.in1 = in1
        self.in2 = in2
        if hasattr(in2,'id') :
            # second in is another object, so connect it
            script.add("#X obj %s %s %s;" % (self.x,self.y,self.op))
            script.connect(in1,self,0)
            script.connect(in2,self,1)            
        else :
            # assume second in is a number
            script.add("#X obj %s %s %s %s;" % (self.x,self.y,self.op,in2))
            script.connect(in1,self,0)
        return self

def mult(*args) : return Op("*").__call__(*args)
def mult_(*args) : return Op("*~").__call__(*args)
def add(*args) : return Op("+").__call__(*args)
def add_(*args) : return Op("+~").__call__(*args)
def sub(*args) : return Op("-").__call__(*args)
def sub_(*args) : return Op("-~").__call__(*args)

               


class Osc(Unit) :

    def __init__(self, oscname) :
        self.oscname = oscname
        self._width = 60
        self._height = 40        
        self.common()
        
    def outPort(self) : return 0
    
    def __call__(self,x) :
        if hasattr(x, 'id') :
            # assume x is another object, so connect it
            script.add("#X obj %s %s %s 0;" % (self.x, self.y, self.oscname)) 
            script.connect(x,self,0)
        else :
            # assume x is a numeric frequency
            script.add("#X obj %s %s %s %s;" % (self.x, self.y, self.oscname, x)) 
        return self
        
        
def sin_(*args) : return Osc("osc~").__call__(*args)
def phasor_(*args) : return Osc("phasor~").__call__(*args)
def noise_(*args) : return Osc("noise~").__call__(*args)

# Filter
class Filter(Unit) :
    def outPort(self) : return 0
    
    def __call__(self,audio_,freq_,res=4) :
        # we assume audio_ and freq_ are signals
        script.connect(audio_,self,0)
        script.connect(freq_,self,1)
        if hasattr(res,"id") :
            # resonance is object too
            script.add("#X obj %s %s vcf~ 440 1;" % (self.x,self.y))
            script.connect(res,self,2)
        else : 
            script.add("#X obj %s %s vcf~ 440 %s;" % (self.x,self.y,res))

        return self
        
def vcf_(*args) : return Filter().__call__(*args)

# Delay
class DelayWrite(Unit) :
    def outPort(self) : return 0
    
    def __call__(self,audio_,delay,name) :
        script.add("#X obj %s %s delwrite~ %s %s;" % (self.x,self.y,name,delay))
        script.connect(audio_,self,0)
        return self

class DelayRead(Unit) :
    def outPort(self) : return 0
    def __call__(self,time_sig,name) :
        script.add("#X obj %s %s vd~ %s;" % (self.x,self.y,name))
        script.connect(time_sig,self,0)
        return self
        
def delaywrite_(*args) : return DelayWrite().__call__(*args)
def delayread_(*args) : return DelayRead().__call__(*args)


    
# Envelopes
def vline_(*args) : return Generic1("vline~").__call__(*args)



# Snapshot
class Snapshot(Unit) :
    def __init__(self) :
        self.name = "snapshot~"
        self.common()
        
    def outPort(self) : return 0
        
    def __call__(self,sig,bangs,*args) :
        arg_string=" ".join(args)
        script.add("#X obj %s %s %s %s;" % (self.x,self.y,self.name,arg_string))
        script.connect(sig,self,0)
        script.connect(bangs,self,0)
        return self

def snapshot(*args) : return Snapshot().__call__(*args)


        
# Generics

def a_float(*args) : return Generic1("float").__call__(*args)
def pack(*args) : return Generic1("pack").__call__(*args)
def mtof(*args) : return Generic1("mtof").__call__(*args)
def mtof_(*args) : return Generic1("mtof~").__call__(*args)        
def clip(*args) : return Generic1("clip").__call__(*args)
def clip_(*args) : return Generic3("clip~").__call__(*args)
def mod(*args) : return Generic1("mod").__call__(*args)


def outlet_(*args) : return Generic1("outlet~").__call__(*args)
def outlet(*args) : return Generic1("outlet").__call__(*args)
def inlet_(*args) : return Generic0("inlet~").__call__(*args)
def inlet(*args) : return Generic0("inlet").__call__(*args)


# User Interface
class UI(Unit) :
    def __init__(self) :
        self._width = 0
        self._height = 0

        self.common()

    def outPort(self) : return 0 # override this if it's not true    
           
    def common(self) :
        self.id = script.nextId()
        self.x, self.y = script.guiNextPosition(self)

def guiCanvas() : script.guiCanvas()


class VNum(UI) :

    def __init__(self) :
        self._width = 40
        self._height = 20
        self.common()

        
    def __call__(self,*args) :        
        script.add("#X floatatom %s %s 5 0 0 0 - - -;" % (self.x,self.y))
        if len(args) > 0 :
            source = args[0]
            script.connect(source,self,0)
        
        return self

def vNum(*args) : return VNum().__call__(*args)          

        
class Bang(UI) :
    def width(self) : return 80
    def height(self) : return 40

    def __call__(self,label) :
        script.add("#X obj %s %s bng 15 250 50 0 empty empty %s 17 7 0 10 -262144 -1 -1;" % (self.x,self.y,label))
        return self        

def bang(*args) : return Bang().__call__(*args)
        


# Subcanvases
class AbstractionSubcanvas(UI) :

    def __init__(self,name,width,height) :
        self.name = name
        self._width = width
        self._height = height
        self.common()
    
    def __call__(self,sources=[]) :
        script.add("#X obj %s %s %s;" % (self.x, self.y, self.name))
        c = 0
        for s in sources :
            # we tie them to the inputs
            script.connect(s,self,c)
            c=c+1
        return self
    
def abstraction(name,width,height,**kwargs) : 
    """Note something unusual here. We take keyword arguments to this function, and look in a kwarg called "sources" for a list 
    of sources for the inlets. We do it this way because we'll also want to be able to pass ordinary arguments to the abstraction
    (though this isn't supported yet) and so we'll put them in a different list"""
    return AbstractionSubcanvas(name,width,height).__call__(**kwargs)

        
# Messages
class VMessage(UI) :
    """ UI Version of Message"""
    def width(self) : return 80
    def height(self) : return 40
    
    def __call__(self,x,y=None) :
        if y :
            script.add("#X msg %s %s %s;" % (self.x, self.y, y))
            script.connect(x,self,0)
        else :
            script.add("#X msg %s %s %s;" % (self.x, self.y, x))
        return self

def vMsg(*args) : return Message().__call__(*args)


# Default initialization messages
def defaultInitialiser(val) :
    return msg(script.getLoadBang(),val)



# Slider
class Slider(UI) :
    def __init__(self,name,wide,high,sep_width) :
        self.name = name
        self.sep_width = sep_width
        self.wide = wide
        self.sep_height = high+20
        self.high = high

        self.common()
                    
    def width(self) : return self.sep_width
    def height(self) : return self.sep_height
    
    def __call__(self,label,lo=0,hi=127,**kwargs) :
        self.label = label        
        self.lo = lo
        self.hi = hi
        script.add("#X obj %s %s %s %s %s %s %s 0 0 empty empty %s -2 -8 0 10 -262144 -1 -1 0 1;" % (self.x, self.y, self.name, self.wide,self.high,lo,hi,self.label))
        if "default" in kwargs :
            script.connect(defaultInitialiser(kwargs["default"]),self,0)

        return self
                
def hslider(*args,**kwargs) : return Slider("hsl",120, 20, 150).__call__(*args,**kwargs)
def vslider(*args,**kwargs) : return Slider("vsl",20, 120, 80).__call__(*args,**kwargs)




# MIDI
class NoteIn(Unit) :
    def outPort(self) : return 0
    
    def __call__(self,*args) :
        script.add("#X obj %s %s notein;" % (self.x,self.y))
        return self
        
def note_in(*args) : return NoteIn().__call__(*args)        
        
class CtlIn(Unit) :
    def outPort(self) : return 0
    
    def __call__(self,*args) :
        script.add("#X obj %s %s ctlin;" % (self.x,self.y))
        return self 
               
def ctl_in(*args) : return CtlIn().__call__(*args) 

       

