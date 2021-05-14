import relativipy as rel
import numpy as np

universe = rel.scene.Universe(screen_size = (7, 7), width=800, height=450)
universe.spacetime_mode = True
universe.axes_origin    = None
universe.screen_mode    = False
universe.t_max = 5

cross_radius = .1

radius = 1
nb_points = 10
t0 = 1
events = np.array([[np.cos(t), np.sin(t), t0 + radius/universe.C] for t in np.linspace(0, 2*np.pi, nb_points, endpoint=False)]) * np.array([radius, radius, 1])
evts = rel.objects.Events(None, universe.C, events, (0, 0, .7))
universe += evts
evts.cross_radius       = cross_radius
evts.slice_cross_radius = 2 * cross_radius

nb_subradius = 5
Rs   = np.linspace(.5, 1, nb_subradius, endpoint=False) * radius
lbd  = np.linspace(0, 1, nb_subradius)
lbd_ = 1 - lbd
color_start = np.array([1, 1, 0])
color_end = np.array([1, 0, 1])
for i, _radius in enumerate(Rs):
    _events = np.array([[np.cos(t), np.sin(t), t0 + _radius/universe.C] for t in np.linspace(0, 2*np.pi, nb_points, endpoint=False)]) * np.array([_radius, _radius, 1])
    _evts = rel.objects.Events(None, universe.C, _events, lbd_[i] * color_start + lbd[i] * color_end)
    universe += _evts
    _evts.cross_radius       = cross_radius
    _evts.slice_cross_radius = 2 * cross_radius

main = rel.objects.Events(None, universe.C, np.array([(0, 0, t0), (0, 0, t0 + 2*radius/universe.C)]), (0, 0, 0))
universe += main
main.cross_radius       = cross_radius
main.slice_cross_radius = 2 * cross_radius

universe += rel.objects.LightCone(universe.C, main.events[0], main.events[1], (.7, .7, 0))
for e in evts.events :
    universe += rel.objects.LightCone(universe.C, e, main.events[1], (0, .7, 0))
    


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
