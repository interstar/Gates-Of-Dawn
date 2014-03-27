# Gates of Dawn
# Python library to generate Pure Data files
# Copyright Phil Jones 2013. Released under GPL 3.0

class Layout : 
    def __init__(self, dx, dy, wrap = 0) :
        self.x = 0      
        self.y = 30
        self.dx = dx
        self.start_dy = dy
        self.dy = dy
        self.wrap = wrap
        self.initLeft = 90
        
    def nextX(self,part) :
        self.x = self.x + part.width()
        if part.height() > self.dy :
            self.dy = part.height()
        if self.wrap and self.x > self.wrap :
            self.cr()                
        return self.x
        
    def nextY(self) :
        self.y = self.y + self.dy
        self.dy = self.start_dy

    def cr(self) :
        self.x = self.initLeft
        self.nextY()                

class Script :
    def __init__(self,w,h,z) :
        self.reset(w,h,z)
        self.lb = None # will become loadbang at end of initialization

    def reset(self,w,h,z) :
        self.width = w
        self.height = h
        self.z = z
        self.x = 20
        self.curY = 0
        self.objects = []
        self.connects = []
        self.ids = -1
        self.ui_layout = Layout(150,40,w)
        

    def getLoadBang(self) :
        # we only have a loadbang if one is called for, via this method
        if not self.lb :
            self.lb = loadbang()
        return self.lb  
                
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
        self.connectFrom(src,src.outPort(),sink,sinkPort)

    def connectFrom(self,src,srcPort,sink,sinkPort) :
        self.addConnect("#X connect %s %s %s %s;" % (src.id,srcPort,sink.id,sinkPort))
        
    def cr(self) : self.ui_layout.cr()

    def guiCanvas(self) :
        # sets up graph-on-canvas around GUI parts
        self.addConnect("#X coords 0 -1 1 1 %s %s 1 %s %s;" % (self.ui_layout.wrap+40, self.ui_layout.y+30, self.ui_layout.initLeft-20, 10))

        
    def out(self) :
        s = """#N canvas 100 100 %s %s %s;\r\n""" % (self.width, self.height, self.z)
        for o in self.objects :
            s = s + o + "\r\n"
        for c in self.connects :
            s = s + c + "\r\n"
        return s

    def __enter__(self) :
        self.clear()
        if self.fName is None :
            self.fName = "default_file.pd"
    
    def __exit__(self,type,value,traceback) :
        with open(self.fName,'w') as f :
            f.write(self.out())
            
script = Script(500,500,10)
def makeFile(fName) :
    script.fName = fName
    return script

class Unit : 
    def __init__(self) :
        self.common()
        
    def common(self) :
        self.id = script.nextId()
        self.x = script.x
        self.y = script.nextY()

class Num(Unit) :

    def outPort(self) : return 0
    
    def __call__(self,*args) :        
        script.add("#X floatatom %s %s 5 0 0 0 - - -;" % (self.x,self.y))
        if len(args) > 0 :
            source = args[0]
            script.connect(source,self,0)
        
        return self

def num(*args) : return Num().__call__(*args)          

class Generic0(Unit) :
    """ Takes 0 input signals """
    def __init__(self,name) :
        self.common()
        self.name = name

    def outPort(self) : return 0

    def __call__(self) :
        script.add("#X obj %s %s %s;" % (self.x, self.y, self.name))
        return self
        
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
def inlet_(*args) : return Generic1("inlet~").__call__(*args)
def inlet(*args) : return Generic("inlet").__call__(*args)


# User Interface
class UI(Unit) :
    def __init__(self) :
        self._width = 0
        self._height = 0

        self.common()
    
    def width(self) : return self._width
    def height(self) : return self._height
           
    def common(self) :
        self.id = script.nextId()
        self.x = script.ui_layout.nextX(self)
        self.y = script.ui_layout.y

def guiCanvas() : script.guiCanvas()

        
class Bang(UI) :
    def outPort(self) : return 0
    def __call__(self,label) :
        script.add("#X obj %s %s bng 15 250 50 0 empty empty %s 17 7 0 10 -262144 -1 -1;" % (self.x,self.y,label))
        return self        

def bang(*args) : return Bang().__call__(*args)
        
def loadbang(*args) : return Generic0("loadbang").__call__(*args)

# Subcanvases
class AbstractionSubcanvas(UI) :

    def __init__(self,name,width,height) :
        self.name = name
        self._width = width
        self._height = height
        self.common()

        
    def outPort(self) : return 0
    
    def __call__(self) :
        script.add("#X obj %s %s %s;" % (self.x, self.y, self.name))
        return self
    
    
def abstraction(name,width,height,*args) : return AbstractionSubcanvas(name,width,height).__call__(*args)

        
# Messages
class Message(UI) :

    def outPort(self) : return 0
    
    def width(self) : return 80
    def height(self) : return 40
    
    def __call__(self,x,y=None) :
        if y :
            script.add("#X msg %s %s %s;" % (self.x, self.y, y))
            script.connect(x,self,0)
        else :
            script.add("#X msg %s %s %s;" % (self.x, self.y, x))
        return self

def msg(*args) : return Message().__call__(*args)


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
        
    def outPort(self) : return 0
    
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

       

