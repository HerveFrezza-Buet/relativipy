import relativipy as rel
import numpy as np

universe = rel.universe.Relativist(screen_size = (6, 3), width=800, height=450) 

barn_color = (1, 0, 0)
barn_center = np.array([1, 0.])
barn_up   = np.array([(.5, .2), (.5, .5), (.7, .5), (0., 1.), (-.7, .5), (-.5, .5), (-.5, .2)]) + barn_center
barn_down = np.array([(-.5, -.2), (-.5, -.5), (.5, -.5), (.5, -.2)])                            + barn_center
universe += rel.objects.Prism(universe, None, (None, None), barn_up,   barn_color)
universe += rel.objects.Prism(universe, None, (None, None), barn_down, barn_color)


# We define two doors, existing (closed) at a specific time interval.
door = np.array([(0., -.2), (0., .2)]) + barn_center
duration = .2
closing_time = 3.75
time_interval = (closing_time-duration/2, closing_time+duration/2) 
universe += rel.objects.Prism(universe, None, time_interval, door + np.array([.5, 0.]), barn_color)
universe += rel.objects.Prism(universe, None, time_interval, door - np.array([.5, 0.]), barn_color)

# Let us add another prism, which is a long horizontal rectangle.
stick_length = 1.05
stick = np.array([(-stick_length/2, -0.1),
                  ( stick_length/2, -0.1),
                  ( stick_length/2,  0.1),
                  (-stick_length/2,  0.1),
                  (-stick_length/2, -0.1)])
# Let us place it, at t=0, at a bottom left position
stick = stick - barn_center
speed = (universe.C/2, 0)
stick_color = (0, .5, 0)
universe += rel.objects.Prism(universe, speed, (None, None), stick, stick_color)

# This is a callback when space is pressed. We set/unset the speed of
# the reference frame that is displayed.
use_local_frame = False
def on_change_frame():
    global use_local_frame
    use_local_frame = not use_local_frame
    if use_local_frame :
        universe.set_view_speed(speed)
    else:
        universe.set_view_speed(None)

universe.on_key_pressed(' ', on_change_frame)
print('press <space> to change the reference frame')
print()

universe.run()
