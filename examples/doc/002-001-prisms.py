import relativipy as rel
import numpy as np


universe = rel.scene.Universe(screen_size = (6, 3), width=800, height=450)

# Let us define 1m-sized squares, not moving, with different life-times.
# Arguments for Prism are local frame speed, speed of light, time range, a list of 2D points, a rgb color.

square_polyline = np.array([(-.5, -.5), (.5, -.5), (.5, .5), (-.5, .5), (-.5, -.5)])
universe += rel.objects.Prism(None, universe.C, (1.0,   2.0), square_polyline                      , (1, 0, 0)) 
universe += rel.objects.Prism(None, universe.C, (None, None), square_polyline + np.array([-1.1, 0]), (0, 1, 0))
universe += rel.objects.Prism(None, universe.C, (1.5,  None), square_polyline + np.array([ 1.1, 0]), (0, 0, 1))

# and run...
universe.run()
