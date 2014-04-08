# Script management

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

def patch(fName) :
    script.fName = fName
    return script

