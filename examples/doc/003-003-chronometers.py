import relativipy as rel
import numpy as np

# This example is the same as 002-002-prism.py, except that we add
# chronometers in each object, n order to visualize its proper
# time. Chronometers are ony a shortcut for defining events.


square_polyline = np.array([(-.5, -.5), (.5, -.5), (.5, .5), (-.5, .5), (-.5, -.5)])
universe = rel.scene.Universe(screen_size = (6, 4), width=800, height=450)
speed = (universe.C/2, universe.C/4)

start_time = 1
end_time   = 4
time_interval = (start_time, end_time)
duration = end_time - start_time
birth_of_red_cube   = np.array([ 1,  .6, start_time]) # The place and time of the birth...
birth_of_green_cube = np.array([-1, -.6, start_time]) # ... in (x, y, t) format (not ct).
tick_period = .25 # 4 impulses per second.


universe += rel.objects.Prism(None,  universe.C, time_interval, square_polyline + birth_of_red_cube  [:2], (1, 0, 0))
universe += rel.objects.Prism(speed, universe.C, time_interval, square_polyline + birth_of_green_cube[:2], (0, 1, 0))

print(birth_of_red_cube)


universe += rel.objects.Chronometer(None,  universe.C, birth_of_red_cube,   tick_period, duration, (1, .75, .75))
universe += rel.objects.Chronometer(speed, universe.C, birth_of_green_cube, tick_period, duration, (.75, 1, .75)) 

# Let us bind the space key to a change of reference frame.

use_green_cube_frame = False
def on_change_frame():
    global use_green_cube_frame
    use_green_cube_frame = not use_green_cube_frame
    if use_green_cube_frame :
        universe.set_view_speed(speed)
    else :
        universe.set_view_speed(None)
        
universe.on_key_pressed(' ', on_change_frame)
print('press <space> to change the reference frame')
print()


# and run...
universe.run()


