import relativipy as rel
import numpy as np

universe = rel.universe.Relativist(screen_size = (10, 10), width=800, height=450)

# The emmission of light from a point is a propagating circular wave,
# travelling at the speed of... light! This forms a cone in the
# spacetime. The starting point of a light cone is a position at a
# specific time, i.e. this is an event. Whereas it propagates forever,
# it is convenient for illustrations to interrupt the light
# propagation. This interruption is triggered by the occurrence of
# another event.

# Warning : The events used for defining light cones are given in (x,
# y, ct) format, not (x, y, t).

# Nota : The weirdness of relativity comes from the fact that the
# travel of light is not sensitive to the frame of reference. As
# opposed to other objects in relativipy, we do not provide the speed
# of a proper frame for light cones definition, it would be a
# non-sense.

# Let us define a set of events.
nb_loops  = 2
nb_events = nb_loops*6 + 1
dt = 1/universe.C # The time need for the light to propagate along 1 meter.
events = np.array([[np.cos(theta), np.sin(theta), rank*dt] for rank, theta in enumerate(np.linspace(0, nb_loops*2*np.pi, nb_events))])
universe.t_max = events[-1][2] + 1
universe.adjust_t_max = True
evts = rel.objects.Events(universe, None, events, (0, 0, 0))
evts.slice_cross_radius = .2 
events = evts.events # we have (x, y, ct) events now... we are ready for light cones definitions.
universe += evts

# We will start a light cone from one event in the list, and stop at the next.
for (start, end) in zip(events[:-1], events[1:]) :
    universe += rel.objects.LightCone(universe, start, end, (.8, .8, 0))

# It is nice to view our scene from moving frames of reference. Let us
# provide a few to the user, by hitting the space key.

v = .25
speeds = [None, (-v, 0), (-v,v), (0, v), (v, v), (v, 0), (v, -v), (0, -v), (-v, -v)]
speed_mode = 0
def on_change_frame():
    global speed_mode
    speed_mode += 1
    if speed_mode >= len(speeds):
        speed_mode = 0
    print('frame speed = {}'.format(speeds[speed_mode]))
    universe.set_view_speed(speeds[speed_mode])
universe.on_key_pressed(' ', on_change_frame)
print('press <space> to change the reference frame')
print()

# That's it.
universe.run()
