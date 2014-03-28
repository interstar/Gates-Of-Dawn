<div style="float: right; padding:10px;">
![Gates of Dawn](http://nooranch.com/blogged/pics/gatesofdawn.jpg)
</div>

Gates Of Dawn
=============


Python library for creating PureData patches.


Why?
----

PureData is a great free synth making toolkit. But I've always found it too laborious to use in practice. I wanted to get into PD, but I think in code. I like my programmer-defined, reusable abstractions. When I'm defining a data-flow network I don't want to be messing around laying out each part in arbitrary x,y co-ordinates.

Gates-of-Dawn lets me write my PD patches as cleanly and succinctly as possible - using function composition - while the computer lays the UI components out for me. Right now it only handles a small subset of PD objects. And is probably way too limited. But I'm already finding it pretty useful for putting synths together.

Quickstart
----------

Make sure you've installed both Python and [PureData](http://puredata.info/) on your machine : 

For a Quickstart on Linux (and probably Mac), do this :

    git clone https://github.com/interstar/Gates-Of-Dawn.git god
    cd god/examples
    ln -s .. god
    python basic_monosynth.py
    pd basic_monosynth.pd


*What Just Happened?*

You created a basic_monosynth using Gates of Dawn and then ran it in PureData.

*I can't hear anything*

Could be the default values in the synth. Make sure PD is capable of producing sound. Make sure the volume of the synth is raised (it defaults to zero) and start playing with the filter values and pitch, you should soon hear something.

Explanation
-----------


So let's look at some simple code examples, introducing some key ideas, while working up to that basic_monosynth.

**Idea #1** : Gates of Dawn uses *function composition* as the way to wire together the units in PureData. 

In PureData traditionally, you'd do something like wire the number coming out of a slider control to the input of an oscillator and then take 
that to the dac audio output. Here's how to express that using Gates of Dawn.

        dac_ ( sin_ ( slider("pitch",0,1000) ) )

To create the slider you call the slider function (giving a label and a range). Then you pass the result of calling that as an argument to the 
sin_ function (which creates an osc~ object in PD). The output of that function is passed as an argument to the dac~. (Note we are now trying to use the convention that functions that represent signal objects (ie. those that have a ~ in their name in PD) will have a _ suffix. This is not ideal but it's the best we can do in Python.)

In Gates of Dawn programs are structured in terms of a bunch of functions which represent either individual PD objects or sub-assemblies of PD objects. You pass as arguments to the functions those things that are upstream and coming in the inlet, and the return value of the function is suitable to be passed to downstream objects.

Things obviously get a bit more complicated than that, but before we go there, let's just grasp the basic outline of a Gates of Dawn program.

**Idea #2** : Files are managed inside _with patch()_ context blocks.

Here's the complete program.

    from god import *

    with patch("hello.pd") as f :
        dac_ ( sin_ ( slider("pitch",0,1000) ) )


We use Python's "with" construction in conjunction with our patch() function to wrap the objects that are going into a file. This is a complete program which defines the simple slider -> oscillator -> dac patch and saves it into a file called "hello.pd"

Try the example above by putting it into a file called hello.py in the examples directory and running it with Python. Then try opening the hello.pd file in PureData.

If you want to create multiple pd files from the same Python program you just have to wrap each in a separate *with patch()* block. 

**Idea #3** : Variables are reusable points in the object graph.

This should be no surprise, given the way function composition works. But we can rewrite that simple patch definition like this :

    s = sin_ ( slider("pitch",0,1000) )
    dac_(s)

The variable s here is storing the output of the sin_ function (ie. the outlet from the oscillator). The next line injects it into the dac.

This isn't useful here, but we'll need it when we want to send the same signal into two different objects later on. 

**NB:** Don't try to reuse variables between one patch block and another. There's a weird implementation behind the scenes and it won't preserve connections between files. (Not that you'd expect it to.) 

**Idea #4** : Each *call* of a Gates of Dawn function makes a new object.

    with patch("hello.pd") as f :
        s = sin_ ( slider("pitch",0,1000) )
        s2 = sin_ ( slider("pitch2",0,1000) )
        dac_(s,s2)


Here, because we call the functions twice, we create two different oscillator objects, each with its own slider control object.

Note that dac_ is an unusual function for Gates of Dawn, in that it takes any number of signal arguments and combines them.

**Idea #5** : You can use Python functions to make cheap reusable sub-assemblies.

Here's where Gates of Dawn gets interesting. We can use Python functions for small bits of re-usable code. 

For example here is simple function that takes a signal input and puts it through a volume control with its own slider.

    def vol(sig,id=1) :
        return mult_(sig,num(slider("vol_%s" % id,0,1)))

Its first argument is any signal. The second is optional and used to make a unique label for the control. 

We can combine it with our current two oscillator example like this : 

    def vol(sig,id=1) :
        return mult_(sig,num(slider("vol_%s" % id,0,1)))

    with patch("hello.pd") as f :
        s = vol (sin_ ( slider("pitch",0,1000) ), "1")
        s2 = vol (sin_ ( slider("pitch2",0,1000) ), "2")
        dac_(s,s2)


Notice that we've defined the vol function once, but we've called it twice, once for each of our oscillators. So we get two copies of this equipment in our patch.

Of course, we can use Python to clean up and eliminate the redundancy here.

    def vol(sig,id=1) :
        return mult_(sig,num(slider("vol_%s" % id,0,1)))

    def vol_osc(id) :
        return vol( sin_( slider("pitch_%s"%id,0,1000) ), id)

    with patch("hello.pd") as f :
       dac_(vol_osc("1"),vol_osc("2"))



**Idea #6** : UI is automatically layed-out (but it's work in progress).

You'll notice, when looking at the resulting pd files, that they're ugly but usable. Gates of Dawn basically thinks that there are two kinds of PD objects. Those you want to interact with and those you don't. All the objects you don't want to see are piled up in a column on the left. All the controls you need to interact with are layed-out automatically in the rest of the screen so you can use them. 

This is still very much work in progress. The ideal for Gates of Dawn is that you should be able to generate everything you want, just from 
the Python script, without having to tweak the PD files by hand later. But we're some way from that at this point. At the moment, if you need to make a simple and usable PD patch rapidly, Gates of Dawn will do it. But it's not going to give you a UI you'll want to use long-term.

**Idea #7** : You still want to use PD's Abstractions

Although Python provides convenient local reuse, you'll still want to use PD's own Abstraction mechanism in the large. Here's an example of 
using it to make four of our simple oscillators defined previously : 

    with patch("hello.pd") as f :
        outlet_ ( vol_osc("$0") )
        guiCanvas()

    with patch("hello_main.pd") as f :
        dac_(
            abstraction("hello",800,50),
            abstraction("hello",800,50),
            abstraction("hello",800,50),
            abstraction("hello",800,50)    
        )


In this example we have two "with patch()" blocks. The first defines a "hello.pd" file containing a single vol_osc() call. (This is the same vol_osc function we defined earlier.)

Note some of the important extras here :
* outlet_() is the function to create a PD outlet object. When the hello.pd patch is imported into our main patch, this is how it will connect to everything else.
* You *must* add a call to guiCanvas() inside any file you intend to use as a PD Abstraction. It sets up the [graph-on-parent](http://en.flossmanuals.net/pure-data/dataflow-tutorials/graph-on-parent/) property in the patch so that the UI controls will appear in any container that uses it.
* Note that we pass $0 to the vol_osc function. $0 is a special variable that is expanded by PD into a *different* random number for every instance of a patch that's being included inside a container. PD doesn't have namespaces so any name you use in an Abstraction is repeated in every copy. This can be problematic. For example a delay may use a named buffer as storage. If you import the same delay Abstraction twice, both instances of the delay will end up trying to use the same buffer, effectively merging the two delayed streams into one. Adding the $0 to the beginning of the name of the buffer will get around this problem as each instance of the delay will get a unique name. In our simple example we don't need to use $0. But I've added it as the label for our vol_osc to make the principle clear.

The second "with patch()" block defines a containing patch called hello_main.pd. It simply imports the hello.pd Abstraction 4 times and passes the four outputs into the dac_.

Note that right now, layout for abstractions is still flaky. So you'll see that the four Abstractions are overlapping. You'll want to go into edit mode and separate them before you try running this example. Once you do that, though, things should work as expected.


Exploring Further
-----------------

basic_monosynth.py shows how to make a real synthesizer, starting with a pair of oscillators, feeds them through a filter, a low-frequency oscillator, a simple delay and finally a volume control. Its pitch is controlled by a slider.

basic_midi_monosynth.py makes the same synth, but controls pitch from a Midi input.

multifile_abstraction_demo.py uses PD's Abstractions to import 3 of these basic_monosynths.

mono_seq.py shows how you can make a simple step-sequencer - prefilled with notes -, and wraps the basic monosynth in AD envelopes for both amplitude and filter-cutoff.

In parts.py and other examples you'll find FM, distortion etc. some of which might even be (partially) working.



Here Comes The Science Bit
--------------------------



Behind the scenes Gates of Dawn does a couple of unorthodox things. 

It uses a module level object called *script* which gets filled with data every time you call a function. It's done this way to reduce the verbosity and visual noise in your program. (Otherwise we'd be writing something like *GOD.dac_(GOD.sin_(GOD.slider("pitch",0,1000)))* the whole time, which would get very tiresome indeed. But it means that you probably shouldn't try to do strange things like use the code in multi-threaded environments or mess around with scope hacking.

Similarly the *patch()* function doesn't do what you expect. It doesn't open a new file object and hand it to you as the context for the "with". Instead it simply primes the script object with the new filename, cleans out the old script information and returns THAT to you. It's when we *exit* the context that the script object opens a new file and dumps the current data into it.

If you want to write your own functions to create PD objects that aren't currently handled, then look first at the Generics in the god.py file. Generic0, Generic1, Generic2 etc. are the classes you use to create PD objects with 0, 1, 2 etc. arguments. In some cases a function to create a new PD object requires nothing more than creating an instance of a GenericX object in Python and calling its call method. If the Generics won't work for you, then you can write your own class, derived from Unit or UI. Look at some of the existing examples. 





