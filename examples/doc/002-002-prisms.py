import relativipy as rel
import numpy as np

square_polyline = np.array([(-.5, -.5), (.5, -.5), (.5, .5), (-.5, .5), (-.5, -.5)])

universe = rel.universe.Relativist(screen_size = (6, 4), width=800, height=450)

# Having one moving polygon is performed by defining a prism in a
# movong frame of reference. In that frame, its speed is null and its
# dimensions are the one you enter, while in the R0 frame, they are
# contracted in the direction of the movement.

speed = (universe.C/2, universe.C/4)


universe += rel.objects.Prism(universe, None,  (1., 4.), square_polyline + np.array([ 1,  .6]), (1, 0, 0))
universe += rel.objects.Prism(universe, speed, (1., 4.), square_polyline + np.array([-1, -.6]), (0, 1, 0))    

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

