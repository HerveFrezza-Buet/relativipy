import relativipy as rel
import numpy as np

universe = rel.universe.Relativist(screen_size = (11, 11), width=800, height=450)
universe.spacetime_mode = False
universe.axes_origin    = None
universe.screen_mode    = False
universe.t_max = 8

cross_radius = .2

radius = .5
points = np.array([(0, -radius), (0, radius)])
universe += rel.objects.Points(universe, None,  (None, None), points, (.7, .7, 1))
universe += rel.objects.Chronometer(universe, None, (0, 0, 0), .25, 10, (1, .7, .7))

dt = 2 * radius * universe.C
t0 = .5
events = np.array([(0, -radius, t0       ),
                   (0,  radius, t0 +   dt),
                   (0, -radius, t0 + 2*dt),
                   (0,  radius, t0 + 3*dt),
                   (0, -radius, t0 + 4*dt)])
evts = rel.objects.Events(universe, None, events, (0, 0, 0))
universe += evts
evts.cross_radius       = cross_radius
evts.slice_cross_radius = 2 * cross_radius

for begin, end in zip(evts.events[:-1], evts.events[1:]):
    universe += rel.objects.LightCone(universe, begin, end, (.7, .7, 0))



speed = universe.C*.70
speeds = np.array([[np.cos(t), np.sin(t)] for t in np.linspace(0, 2*np.pi, 12, endpoint=False)]) * speed
motion_mode = False

def on_switch():
    global motion_mode
    motion_mode = not motion_mode
    if motion_mode:
        universe.set_view_speed(speeds[current_speed_idx])
    else:
        universe.set_view_speed(None)
        
current_speed_idx = 0
def on_next() :
    global current_speed_idx
    global motion_mode
    motion_mode = True
    current_speed_idx += 1
    if current_speed_idx >= len(speeds):
        current_speed_idx = 0
    universe.set_view_speed(speeds[current_speed_idx])

universe.on_key_pressed(' ', on_switch)
universe.on_key_pressed('n', on_next)
print('<space> : null/non-null speed')
print('n       : next speed')
print()

universe.run()
