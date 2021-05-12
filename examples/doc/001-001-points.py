import relativipy as rel # The relativipy library
import numpy as np       # Numpy for smart numerics.

# Let us define our 2D space as 6mx3m area. We display it on a 800x450
# window.
universe = rel.scene.Universe(screen_size = (6, 3), width=800, height=450)

# Here are global settings, default values are often ok, but they are
# listed here with the default values for the sake of description.

universe.spacetime_mode = True                     # Do we display 3D at start ?
universe.screen_mode    = True                     # Do we display the screen in the 3D mode ?
universe.bgcolor        = (0.30, 0.30, 0.35, 1.00) # rgba background color.

universe.C              = 1                        # the (fake) speed of light in m/s.
universe.t_max          = 5                        # The end of time in the simulation
universe.adjust_t_max   = False                    # Do we adjust t_max when the frame of reference changes ?

# Ok, now we are ready to add objects on our world. Let us display two
# dots, one still an the other moving... Hey, in relativity there is
# not absolute frame... both can be considered as still !!!

# In relativipy, we consider arbitrarily a R0 frame of reference where
# events (x, y t) are described. It is the one associated to the (vx,
# vy) = (0, 0) null speed. All objects defined in relativipy are,
# behind the scene, described in the same frame of reference R0.

# Let us define our first point in R0

points = np.array([[0, 0]]) # This is a list of 1 point, a point being a (x, y) pair.

# This is the speed of the frame of reference in which the points are
# defined. Here, None means the null speed, i.e. we are considering
# R0.
speed  = None

# The time interval (tmin, tmax) defines when the object exists. The specific value tmin=None means that the object has always been there so far (tmin = -infinity), and tmax=None means that it is immortal (tmax = +infinity).
time_interval = (None, None)

color = (0., .7, .7)

# Let us create the object, sets some of its features, and add it to our universe.
obj = rel.objects.Points(speed, universe.C, time_interval, points, color)
obj.cross_radius = .05 # We set the size for the cross associated to the point to the default value here.
universe += obj

# Let us now add another point, moving at C/2 meters per seconds to the right.
speed = (universe.C/2, 0.) # vx, vy

# The idea is to define the same as previously, i.e. a still point,
# but passing a not None speed to the object construction, telling
# that its definition is made withing a moving frame of reference (the
# proper frame indeed).
universe += rel.objects.Points(speed, universe.C, time_interval, points, (.7, 0., .7))

# This is it for our 2 objects. Now let us provide the user with the
# possibility to stand in R0 or in the moving frame, where our second
# point is still.

i_am_in_R0 = True
def on_change_frame():          # This will be called when the user hits 
    global i_am_in_R0           # the space key. In this case...
    i_am_in_R0 = not i_am_in_R0 # ... we change the viewing mode
    if i_am_in_R0 :
        universe.set_view_speed(None)
    else:
        universe.set_view_speed(speed)

# We tell the interface to bind the space key to our change mode
# function.
universe.on_key_pressed(' ', on_change_frame)
print('press <space> to change the reference frame')
print()

# That's it ! Do not forget to hit the space key...
universe.run()

# You will notice that time event (x=0, y=0, t=0) are the same in both
# frames. Indeed, we define moving frames by their moving speed
# relative to R0, but the assumption is made that the frames of
# reference coincide for t=0. This is what the Lorentz transform we
# use behind the scene implies.
                           
