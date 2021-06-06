import relativipy as rel
import numpy as np

universe = rel.universe.Relativist(screen_size = (4, 2), width=800, height=450)

Xampl = 10
Xnbs  = 61
Xs = np.linspace(-Xampl, Xampl, Xnbs)
dy = .05

current_speed = (universe.C*.75, 0)
atoms = np.array([[x, dy] for x in Xs])
atoms = rel.objects.Points(universe, None, (None, None), atoms, (1, 0, 0))

dilatation_coef = 1.6 # Ok... I have tweaked it empirically.
electrons = np.array([[x, -dy] for x in Xs*dilatation_coef])
electrons = rel.objects.Points(universe, current_speed, (None, None), electrons, (0, .75, 0))

electrons.cross_radius = .02
atoms.cross_radius     = .02
universe += electrons
universe += atoms

use_electrons_frame = False
def on_change_frame():
    global use_electrons_frame
    use_electrons_frame = not use_electrons_frame
    if use_electrons_frame :
        universe.set_view_speed(current_speed)
    else :
        universe.set_view_speed(None)
        
universe.on_key_pressed(' ', on_change_frame)
print('press <space> to change the reference frame')
print()

universe.run()
