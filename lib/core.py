# Gates of Dawn
# Python library to generate Pure Data files
# Copyright Phil Jones 2013. Released under GPL 3.0

# Core routines for handling script, layout and basic Unit

class MaxMeasure :
    # way to measure the build up of something eg. line width and to track the maximum
    def __init__(self,current=0) :
        self.val = 0
        self.currentMax = current
        
    def add(self,x) :
        self.val = self.val + x
        
    def reset(self) :
        if self.val > self.currentMax :
            self.currentMax = self.val
        self.val = 0


class Layout : 
    def __init__(self, top, left, dx, width) :
        self.reset(top,left,dx,width)
        
    def reset(self,top,left,dx,width) :
        self.top = top
        self.left = left
        self.dx = dx
        self.width = width
        self.measureWidth = MaxMeasure(width)
        self.measureHeight = MaxMeasure()
        self.x = left
        self.y = top
        self.dropY = 0

        
    def nextPosition(self,part=None) :
        # returns the position for the next part, and if there's a part, updates the x and y for the next time
        rx,ry = self.x, self.y

        if part :
            if part.height() > self.dropY :
                self.dropY = part.height()
            
            self.x = self.x + part.width()
            self.measureWidth.add(part.width())

            if self.x > self.left + self.width :
                self.cr()
                            
        return rx,ry
        
    def cr(self) :
        self.x = self.left        
        self.y = self.y + self.dropY + 20
        self.measureHeight.add(self.dropY+20)
        self.measureWidth.reset()
        
    def getHeight(self) : return self.y - self.top
    def getWidth(self) : return self.width
    def canvasWidth(self) : return self.measureWidth.currentMax + 10
    def canvasHeight(self) : 
        self.cr()
        self.measureHeight.reset()
        return self.measureHeight.currentMax


class Patch :
    def __init__(self,name,layout) :
        self.reset(name,layout)
        self.lb = None # will become loadbang at end of initialization

    def reset(self,name,layout) :
        self.fName = name
        self.objects = []
        self.connects = []
        self.ids = -1
        self.gui_layout = layout
        self.hidden_layout = Layout(5,10,40,50)

    def getLoadBang(self) :
        # we only have a loadbang if one is called for, via this method
        if not self.lb :
            self.lb = loadbang()
        return self.lb  
                
    def nextId(self) :
        self.ids = self.ids + 1
        return self.ids
            
    def add(self,s) :
        self.objects.append(s)
    
    def addConnect(self,s) :
        self.connects.append(s)
        
    def connect(self,src,sink,sinkPort) :
        self.connectFrom(src,src.outPort(),sink,sinkPort)

    def connectFrom(self,src,srcPort,sink,sinkPort) :
        self.addConnect("#X connect %s %s %s %s;" % (src.id,srcPort,sink.id,sinkPort))
        
    def hiddenNextPosition(self,part=None) : return self.hidden_layout.nextPosition(part)

    def guiNextPosition(self,part=None) :  return self.gui_layout.nextPosition(part)

    def guiCanvas(self) :
        # sets up graph-on-canvas around GUI parts
        self.addConnect("#X coords 0 -1 1 1 %s %s 1 %s %s;" % 
                        (self.gui_layout.canvasWidth(), self.gui_layout.canvasHeight(), self.gui_layout.left-10, self.gui_layout.top-15))

    def windowWidth(self) : 
        return self.gui_layout.getWidth() + 20 + self.hidden_layout.getWidth()
        
    def windowHeight(self) : 
        return self.gui_layout.canvasHeight()
        
    def out(self) :
        s = """#N canvas 100 100 %s %s %s;\r\n""" % (self.windowWidth(), self.windowHeight(), self.fName)
        for o in self.objects :        
            s = s + o + "\r\n"
        for c in self.connects :
            s = s + c + "\r\n"
        return s

    def __enter__(self) :        
        if self.fName is None :
            self.fName = "default_file.pd"
    
    def __exit__(self,type,value,traceback) :
        with open(self.fName,'w') as f :
            f.write(self.out())
            
script = Patch("dummy",Layout(150,50,40,300))

def patch(fName,layout = None) :
    if layout is None : 
        layout = Layout(150,50,40,300)
    script.reset(fName,layout)    
    return script

####################

class Unit : 
    def __init__(self) :
        self._width = 80
        self._height = 20
        self.common()

    def width(self) : return self._width
    def height(self) : return self._height
        
    def common(self) :
        self.id = script.nextId()
        self.x, self.y = script.hiddenNextPosition(self)

class Generic0(Unit) :
    """ Takes 0 input signals """
    def __init__(self,name) :
        self._width = 60
        self._height = 40    
        self.common()
        self.name = name

    def outPort(self) : return 0

    def __call__(self) :
        script.add("#X obj %s %s %s;" % (self.x, self.y, self.name))
        return self

# this has to be defined in this file so that we can handle circular reference between it and Patch class
def loadbang(*args) : return Generic0("loadbang").__call__(*args)
