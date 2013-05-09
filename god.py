# Gates of Dawn
# Python library to generate Pure Data files
# Copyright Phil Jones 2013. Released under GPL 3.0

class Layout : 
    def __init__(self, dx, dy, wrap = 0) :
        self.x = 0
        self.y = 30
        self.dx = dx
        self.dy = dy
        self.wrap = wrap
        
    def nextX(self) :
        self.x = self.x + self.dx
        if self.wrap and self.x > self.wrap :
            self.cr()                
        return self.x
        
    def nextY(self) :
        self.y = self.y + self.dy

    def cr(self) :
        self.x = 150
        self.nextY()
                

class Script :
    def __init__(self,w,h,z) :
        self.reset(w,h,z)

    def reset(self,w,h,z) :
        self.width = w
        self.height = h
        self.z = z
        self.x = 20
        self.curY = 0
        self.objects = []
        self.connects = []
        self.ids = -1
        self.ui_layout = Layout(150,50,w)
                
    def nextId(self) :
        self.ids = self.ids + 1
        return self.ids
    
    def nextY(self) :
        self.curY = self.curY + 40
        return self.curY
        
    def add(self,s) :
        self.objects.append(s)
    
    def addConnect(self,s) :
        self.connects.append(s)
        
    def clear(self) :
        self.reset(self.width,self.height,self.z)

    def connect(self,src,sink,sinkPort) :
        self.addConnect("#X connect %s %s %s %s;" % (src.id,src.outPort(),sink.id,sinkPort))
        
    def cr(self) : self.ui_layout.cr()
        
    def out(self) :
        s = """#N canvas 100 100 %s %s %s;\r\n""" % (self.width, self.height, self.z)
        for o in self.objects :
            s = s + o + "\r\n"
        for c in self.connects :
            s = s + c + "\r\n"
        return s
                    
script = Script(800,500,10)

class Unit : 
    def __init__(self) :
        self.common()
        
    def common(self) :
        self.id = script.nextId()
        self.x = script.x
        self.y = script.nextY()
        
class Generic(Unit) :
    def __init__(self,name) :
        self.common()
        self.name = name
        
    def outPort(self) : return 0
    
    def __call__(self,in1,*args) :
        arg_string = " ".join(args)
        script.add("#X obj %s %s %s %s;" % (self.x, self.y, self.name, arg_string))
        script.connect(in1,self,0)
        return self

class Dac(Unit) :
    def __call__(self,*args) :
        script.add("#X obj %s %s dac~;" % (self.x,self.y))
        for a in args :
            script.connect(a,self,0)
            script.connect(a,self,1)
        return self
        
def dac(*args) : return Dac().__call__(*args)


# Operators
class Op(Unit) :
    def __init__(self,operator) :
        self.op = operator
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
def sigmult(*args) : return Op("*~").__call__(*args)
def add(*args) : return Op("+").__call__(*args)
def sigadd(*args) : return Op("+~").__call__(*args)
def sub(*args) : return Op("-").__call__(*args)
def sigsub(*args) : return Op("-~").__call__(*args)


class Num(Unit) :

    def outPort(self) : return 0
    
    def __call__(self,*args) :        
        script.add("#X floatatom %s %s 5 0 0 0 - - -;" % (self.x,self.y))
        if len(args) > 0 :
            source = args[0]
            script.connect(source,self,0)
        
        return self

def num(*args) : return Num().__call__(*args)          
               


class Osc(Unit) :

    def __init__(self, oscname) :
        self.oscname = oscname
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
        
        
def sin(*args) : return Osc("osc~").__call__(*args)
def phasor(*args) : return Osc("phasor~").__call__(*args)
def noise(*args) : return Osc("noise~").__call__(*args)

# Filter
class Filter(Unit) :
    def outPort(self) : return 0
    
    def __call__(self,sigAudio,sigFreq,res=4) :
        # we assume sigAudio and sigFreq are signals
        script.connect(sigAudio,self,0)
        script.connect(sigFreq,self,1)
        if hasattr(res,"id") :
            # resonance is object too
            script.add("#X obj %s %s bp~ 440 1;" % (self.x,self.y))
            script.connect(res,self,2)
        else : 
            script.add("#X obj %s %s bp~ 440 %s;" % (self.x,self.y,res))

        return self
        
def vcf(*args) : return Filter().__call__(*args)

# Delay
class DelayWrite(Unit) :
    def outPort(self) : return 0
    
    def __call__(self,sigAudio,delay,name) :
        script.add("#X obj %s %s delwrite~ %s %s;" % (self.x,self.y,name,delay))
        script.connect(sigAudio,self,0)
        return self

class DelayRead(Unit) :
    def outPort(self) : return 0
    def __call__(self,time_sig,name) :
        script.add("#X obj %s %s vd~ %s;" % (self.x,self.y,name))
        script.connect(time_sig,self,0)
        return self
        
def delaywrite(*args) : return DelayWrite().__call__(*args)
def delayread(*args) : return DelayRead().__call__(*args)

def simple_delay(sig,max_delay,name) :
    write = delaywrite(sig,max_delay+1,name)
    read = delayread(slider("%s_feedback_time"%name,0,max_delay),name)
    fback = sigmult(read,slider("%s_feedback_gain"%name,0,0.9))
    script.connect(fback,write,0)
    return read
    
# Envelopes
def vline(*args) : return Generic("vline~").__call__(*args)

        
# Generics

def a_float(*args) : return Generic("float").__call__(*args)
def pack(*args) : return Generic("pack").__call__(*args)
def mtof(*args) : return Generic("mtof").__call__(*args)
def sigmtof(*args) : return Generic("mtof~").__call__(*args)        



# User Interface
class UI(Unit) :
    def __init__(self) :
        self.common()
        
    def common(self) :
        self.id = script.nextId()
        self.x = script.ui_layout.nextX()
        self.y = script.ui_layout.y
        
class Bang(UI) :
    def outPort(self) : return 0
    def __call__(self,label) :
        script.add("#X obj %s %s bng 15 250 50 0 empty empty %s 17 7 0 10 -262144 -1 -1;" % (self.x,self.y,label))
        return self        

def bang(*args) : return Bang().__call__(*args)
        
# Messages

class Message(UI) :

    def outPort(self) : return 0
    
    def __call__(self,x,y=None) :
        if y :
            script.add("#X msg %s %s %s;" % (self.x, self.y, y))
            script.connect(x,self,0)
        else :
            script.add("#X msg %s %s %s;" % (self.x, self.y, x))
        return self

def msg(*args) : return Message().__call__(*args)


# Slider

class Slider(UI) :
    def outPort(self) : return 0
    
    def __call__(self,label,lo=0,hi=127,*args) :
        self.label = label
        self.lo = lo
        self.hi = hi
        script.add("#X obj %s %s hsl 128 20 %s %s 0 0 empty empty %s -2 -8 0 10 -262144 -1 -1 0 1;" % (self.x, self.y,lo,hi,self.label))
        return self
                
def slider(*args) : return Slider().__call__(*args)

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
        
if __name__ == '__main__' :
    import unittest
    
    class TestBasic(unittest.TestCase) :
        def test1(self) :
            script.clear()
            self.assertEquals(script.out(),"#N canvas 100 100 100 100 10;\r\n")
            out = dac(sin(880))
            self.assertEquals(script.out(), """#N canvas 100 100 100 100 10;\r
#X obj 50 40 osc~ 880;\r
#X obj 50 80 dac~;\r
#X connect 0 0 1 0;\r
#X connect 0 0 1 1;\r
""")

        def test2(self) :
            script.clear()
            out = dac(sigmult(sin(440),0.3))
            self.assertEquals(script.out(),
"""#N canvas 100 100 100 100 10;\r
#X obj 50 40 osc~ 440;\r
#X obj 50 80 *~ 0.3;\r
#X obj 50 120 dac~;\r
#X connect 0 0 1 0;\r
#X connect 1 0 2 0;\r
#X connect 1 0 2 1;\r
""")

    unittest.main()
    
    
