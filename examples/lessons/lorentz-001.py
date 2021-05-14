import relativipy as rel
import numpy as np

universe = rel.scene.Universe(screen_size = (11, 11), width=800, height=450)
universe.spacetime_mode = False
universe.axes_origin    = None
universe.screen_mode    = False
universe.t_max = 8

radius = .5
points = np.array([(0, -radius), (0, radius)])
universe += rel.objects.Points(None,  universe.C, (None, None), points, (.7, .7, 1))
universe += rel.objects.Chronometer(None, universe.C, (0, 0, 0), .25, 10, (1, .7, .7))

dt = 2 * radius * universe.C
t0 = .5
events = np.array([(0, -radius, t0       ),
                   (0,  radius, t0 +   dt),
                   (0, -radius, t0 + 2*dt),
                   (0,  radius, t0 + 3*dt),
                   (0, -radius, t0 + 4*dt)])
evts = rel.objects.Events(None, universe.C, events, (0, 0, 0))
universe += evts
evts.cross_radius       = .25
evts.slice_cross_radius = .5

for begin, end in zip(evts.events[:-1], evts.events[1:]):
    universe += rel.objects.LightCone(universe.C, begin, end, (.7, .7, 0))



speed = universe.C*.70
speeds = np.array([[np.cos(t), np.sin(t)] for t in np.linspace(0, 2*np.pi, 12, endpoint=False)]) * speed

current_speed_idx = 0
def on_next() :
    global current_speed_idx
    current_speed_idx += 1
    if current_speed_idx >= len(speeds):
        current_speed_idx = 0
    universe.set_view_speed(speeds[current_speed_idx])

universe.on_key_pressed(' ', lambda: universe.set_view_speed(None))
universe.on_key_pressed('n', on_next)
print('<space> : null speed')
print('n       : next speed')
print()

universe.run()
