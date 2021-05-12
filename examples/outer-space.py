import relativipy as rel

universe = rel.scene.Universe(screen_size = (4., 3.)) # The (width, height) of the 2D screen in meters.

# As prompted by the message on the terminal, press 't' in order to
# swicth between spactime and time modes, or 's' to toggle the display
# of the screen.
universe.run()
