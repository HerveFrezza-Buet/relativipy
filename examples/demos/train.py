import relativipy as rel
import numpy as np

universe = rel.scene.Universe(screen_size = (6, 3), width=800, height=450)
universe.spacetime_mode = False

train_speed    = (universe.C*.75, 0)
universe.force_view_speed(train_speed) # No smooth transition...

start_pos = np.array([-1, 0])
height = .7
train = np.array([[-1, height + .02], [1, height + .02], [1.5, 0], [1.5, -.2], [-1, -.2],[-1, height + .02]] , dtype=np.float32)
bulb  = np.array([[-.1, -.2], [-.1, -.02], [.1, -.02], [.1, -.2]])
universe += rel.objects.Prism(train_speed, universe.C, (None, None), train + start_pos, (1, 0, 0))
universe += rel.objects.Prism(train_speed, universe.C, (None, None), bulb  + start_pos, (1, 0, 0))
universe += rel.objects.Chronometer(train_speed, universe.C, (0., .3, 0), .2, universe.t_max, (.5, .5, .5))

mirror = np.array([[-.25, height], [.25, height]], dtype = np.float32)
universe += rel.objects.Prism(train_speed, universe.C, (None, None), mirror + start_pos, (0, 0, 1))

event_offset = np.array([start_pos[0], start_pos[1], 1])
events = np.array([[0, 0, 0], [0, height, universe.C * height], [0, 0, 2 * universe.C * height]]) + event_offset
events = rel.objects.Events(train_speed, universe.C, events, (0, 0, 0))
universe += events
events = events.events

universe += rel.objects.LightCone(universe.C, events[0], events[1], (0, .8, 0))
universe += rel.objects.LightCone(universe.C, events[1], events[2], (0, .8, 0))

universe.t_max = events[2][2]/universe.C + 0.5
universe.adjust_t_max = False

# Let us add rails
universe += rel.objects.Prism(None, universe.C, (None, None), np.array([[-10, -.25], [10, -.25]]), (0, 0, 0))
bars = np.array([[x, -.25] for x in np.linspace(-10, 10, 100)])
bars = rel.objects.Points(None,  universe.C, (None, None), bars, (0, 0, 0))
bars.cross_radius = .05
universe += bars

use_train_frame = True
        
def on_change_frame():
    global use_train_frame
    use_train_frame = not use_train_frame
    if use_train_frame :
        universe.set_view_speed(train_speed)
    else :
        universe.set_view_speed(None)
        
universe.on_key_pressed(' ', on_change_frame)
print('press <space> to change the reference frame')
print()

universe.run()
