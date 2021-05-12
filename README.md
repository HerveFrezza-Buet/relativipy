# 3D simulation of restricted relativity stories

## What is relativipy ?

Restriced relativity, with the concepts of space and time that change according to the point of observation, with the notion of 4D spacetime, is difficult to understand for the public, for students, etc...

The library relativipy offers python tools in order to visualize the spacetime and its transformation by the Lorentz transform. It is oriented toward the setting up of pedagogical materials, for any purpose.

The space considered in relativipy is 2D, so the spacetime is 3D... it can be visualized by 3D graphics ! (as opposed to the 4D real spacetime...).

The rendering is based on [glumpy](https://glumpy.github.io/) by Nicolas Rougier.

## Installation

This projects is based on [glumpy](https://glumpy.github.io/). On ubuntu, you may need to install glfw with glumpy.

```
sudo apt install libglfw3
```

This is an example of a glumpy installation on your computer from the sources.

```
git clone https://github.com/glumpy/glumpy.git
cd glumpy
python3 setup.py install --user
```

Then, you can get relativipy by cloning this git and proceed to relativipy installation on your computer.

```
git clone git@github.com:HerveFrezza-Buet/relativipy.git
cd relativipy
python3 setup.py install --user
```

Then you may be able to run the examples in the 'examples' directory.

```
cd examples/
python3 some-example.py
```

## Getting started

This is the box opening phase, check that you can run the basics and understand how to use it. Go into the example directory, and start the "empty universe" example.

```
cd examples/
python3 outer-space.py
```

You should see an empty timespace, with the 2D current time slice moving from star time to end time, periodically. Nothing is in that space... it is empty.

Try to press 's' (screen) several times, it will toggle the display of the moving screen. You can move around the view with the mouse.

Try to press 't' (time) several times, it toggles the spacetime versus 2D animated space view.

Thanks to glumpy, you can benefit from many extra features. For example, you can record the movie if the experiment. To do so, launch

```
python3 outer-space.py --record
```

Ok... for an empty space, this is not so exciting. Have a look at the `outer-space.py` code if you intend to use the library for building up your own experiments. Then read and execute the examples in the `doc` section... they am at providing you with a good understanding of relativipy possibilities and how to use them.

If you just want to run nice demos, explore de `demo` section and run the scripts.


## Documentation

As previously said, read the examples in the `doc` section. It could be easier if you read them  in the order suggested by the filenames. You need numpy basics to understand the examples.

## Demos

The `demo` section may be filled with more demos in the future. Try them all !



