import relativipy as rel
import numpy as np

universe = rel.universe.Relativist(screen_size = (6, 4), width=800, height=450)

# Let us define 2 events for display.
events = np.array([[1, 1, 1], [1, 1, 3]])
speed = None
universe += rel.objects.Events(universe, speed, events, (0, 0, 0))

# Now, let us define two notifiers. They aim at calling a function
# when an event occurs.

universe += rel.objects.Notifier(universe, speed, events[0], lambda t: print('A at {} s'.format(t)))
universe += rel.objects.Notifier(universe, speed, events[1], lambda t: print('B at {} s'.format(t)))

universe.on_restart(lambda: print('The simulation restarts'))

# This allows for selecting a viriety of speeds for the viewing frame
# of reference.
v = .25
speeds = [None, (-v, 0), (-v,v), (0, v), (v, v), (v, 0), (v, -v), (0, -v), (-v, -v)]
speed_mode = 0
def on_change_frame():
    global speed_mode
    speed_mode += 1
    if speed_mode >= len(speeds):
        speed_mode = 0
    print('frame speed = {}'.format(speeds[speed_mode]))
    universe.set_view_speed(speeds[speed_mode])
universe.on_key_pressed(' ', on_change_frame)
print('press <space> to change the reference frame')
print()

# That's it.
universe.run()
