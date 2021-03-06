import relativipy as rel
import numpy as np

universe = rel.universe.Relativist(screen_size = (10, 10), width=800, height=450)
universe.spacetime_mode = True
universe.axes_origin    = None
universe.screen_mode    = False
universe.t_max = 10

cross_radius = .1

def make_cone(start_event, radius):
    global universe
    nb_points = 20
    events = np.array([[np.cos(t), np.sin(t), radius/universe.C] for t in np.linspace(0, 2*np.pi, nb_points, endpoint=False)]) * np.array([radius, radius, 1]) + start_event
    evts = rel.objects.Events(universe, None, events, (0, 0, .7))
    universe += evts
    evts.cross_radius       = cross_radius
    evts.slice_cross_radius = 2 * cross_radius

    main = rel.objects.Events(universe, None, np.array([(0, 0, 0), (0, 0, 2*radius/universe.C)]) + start_event, (0, 0, 0))
    universe += main
    main.cross_radius       = cross_radius
    main.slice_cross_radius = 2 * cross_radius

    universe += rel.objects.LightCone(universe, main.events[0], main.events[1], (.7, .7, 0))

    
R = np.linspace(-2, 2, 3)
T = np.linspace( 2, 5, 3)
starts = np.array([[x, y, t] for x in R for y in R for t in T])
for start in starts:
    make_cone(start, .5)

    
speed = universe.C*.50
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
