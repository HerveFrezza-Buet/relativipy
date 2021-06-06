import relativipy as rel
import numpy as np

universe = rel.universe.Relativist(screen_size = (6, 4), width=800, height=450)

# In restricted relativity, events are points in the spacetime,
# i.e. (x, y, ct) triplets with our bidimentional space. It is
# convenient to define them as (x, y, t) points (rather than (x, y,
# ct). As for other elements, they are always defined with ther proper
# positon and times, but we notify which frame (i.e. which speed) is
# considered.

# These are (x, y, t) events.
events = np.array([[np.cos(theta), np.sin(theta), theta/(2*np.pi)] for theta in np.linspace(0, 8*np.pi, 100)])

# Let us build an Events relativipy object for them. None is for R0, as usual.
evts = rel.objects.Events(universe, None, events, (0, .7, .7))

# Events appear as a 3D crosses, that sparkle when they actually
# occur. You can adjust these features, the default are set here for
# the sake of illustration.
evts.cross_radius       = .05 # The radius of the cross representing the event in the 3D view.
evts.slice_cross_radius = .10 # The radius of the cross in the 2D view, when the event occurs.
evts.spot_duration      = .30 # The duration (in sec) of the event extinction.

# Moreover, the events in (x, y, ct) notation, in the R0 frame, have
# been computed and are available in the events attribute.
print(evts.events[3])

# Let us add this event set in the simulation.
universe += evts

# As usual, let us define the same events in a moving proper frame of reference.
speed = (universe.C/2, -universe.C/4)
universe += rel.objects.Events(universe, speed, events, (.7, 0, .7))

i_am_in_R0 = True
def on_change_frame():          
    global i_am_in_R0           
    i_am_in_R0 = not i_am_in_R0 
    if i_am_in_R0 :
        universe.set_view_speed(None)
    else:
        universe.set_view_speed(speed)

universe.on_key_pressed(' ', on_change_frame)
print('press <space> to change the reference frame')
print()

# That's it ! Do not forget to hit the space key...
universe.run()

