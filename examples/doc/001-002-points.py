import relativipy as rel
import numpy as np

universe = rel.universe.Relativist(screen_size = (6, 3), width=800, height=450)
universe.adjust_t_max = True
universe.t_max        = 5

max_speed = np.array([universe.C/3, 0])
xy = np.array([[0, y] for y in np.linspace(-.5, .5, 5)])

color_start = np.array([.9, .1, .5])
color_end   = np.array([.1, .5, .9])

time_interval = (1, universe.t_max - .5) 

# Ok let ius create many point groups.
for l in np.linspace(0, 1, 5) :
    universe +=rel.objects.Points(universe,
                                  (2*l - 1) * max_speed, # from -max_speed to max_speed
                                  time_interval,
                                  xy,
                                  (1-l) * color_start + l * color_end)

mode_moving_frame = 0
def on_change_frame():
    global mode_moving_frame
    mode_moving_frame += 1
    if mode_moving_frame > 1:
        mode_moving_frame = -1
    if mode_moving_frame == 0:
        universe.set_view_speed(None)
    else:
        universe.set_view_speed(mode_moving_frame * max_speed)
        
universe.on_key_pressed(' ', on_change_frame)
print('press <space> to change the reference frame')
print()

universe.run()
