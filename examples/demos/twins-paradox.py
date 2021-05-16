import relativipy as rel
import numpy as np


universe = rel.scene.Universe(screen_size = (3, 15), width=800, height=450)
universe.spacetime_mode   = False
universe.show_prism_lines = False
universe.t_max            = 10

human_size           = 1
ground_level         = -human_size/2
travel_speed         = universe.C*.75
travel_go_duration   = 2
travel_back_duration = travel_go_duration
chrono_period        = .25

universe.axes_origin = (-1, ground_level)

head  = np.array([[np.sin(t), -np.cos(t)] for t in np.linspace(0, 2*np.pi, 11)])
left  = np.array([(-1, 0), (-1, 3), (-1, 2), (-2, 2), (-2, 4)])
right = np.flip((left * np.array([-1, 1])), axis=0)
human = np.vstack((left, head + np.array([0, 5]), right, np.array([left[0]]))) * human_size/6


ship = np.array([(-5, -4), (-3, -1), (-3, 4), (0, 5), (3, 4), (3, -1), (5, -4), (-5, -4)])
universe += rel.objects.Prism((0, travel_speed), universe.C, (None, None), ship, (.2, .2, .2))

twin_start_position = (0, ground_level)
twin = human + twin_start_position

olivier    = rel.objects.Prism(None,              universe.C, (None, None              ), twin, (1, 0, 0))
herve_go   = rel.objects.Prism((0, travel_speed), universe.C, (0,    travel_go_duration), twin, (0, 0, 1))

start_evts     = rel.objects.Events(None             , universe.C, np.array([[0, 0,                   0 ]]), (0, 0, 0))
turn_back_evts = rel.objects.Events((0, travel_speed), universe.C, np.array([[0, 0, travel_back_duration]]),  (0, 0, 0))

turn_back_xyct_R0 = turn_back_evts.events
turn_back_date_R0 = turn_back_xyct_R0[0][2] / universe.C

end_evts = rel.objects.Events(None, universe.C, np.array([[0, 0, 2 * turn_back_date_R0]]), (0, 0, 0))

L_R0_to_Rback        = rel.lorentz.direct(np.array([0, -travel_speed]), universe.C)
turn_back_xyct_Rback = rel.lorentz.transform(L_R0_to_Rback, turn_back_xyct_R0)

U_turn_xyt_Rback = turn_back_xyct_Rback[0] * np.array([1, 1, 1/universe.C])
herve_back = rel.objects.Prism((0, -travel_speed), universe.C, (U_turn_xyt_Rback[2], U_turn_xyt_Rback[2] + travel_back_duration), twin + U_turn_xyt_Rback[:2], (0, 0, 1))

universe += olivier
universe += herve_go
universe += herve_back

start_xyt_R0 = start_evts.events[0] * np.array([1, 1, 1/universe.C])
nb_ticks_A = 6
nb_ticks_B = 13
nb_ticks_C = 5
epsilon = 1e-3
start_evt = start_xyt_R0
end_time   = start_evt[2] + nb_ticks_A * chrono_period
chrono_olivier_A = rel.objects.Chronometer(None, universe.C, start_evt, chrono_period, end_time - start_evt[2] - epsilon, (1, .7, .7))
start_evt[2] = end_time
end_time += nb_ticks_B * chrono_period
chrono_olivier_B = rel.objects.Chronometer(None, universe.C, start_evt, chrono_period, end_time - start_evt[2] - epsilon, (.5, .2, .2))
start_evt[2] = end_time
end_time += nb_ticks_C * chrono_period
chrono_olivier_C = rel.objects.Chronometer(None, universe.C, start_evt, chrono_period, end_time - start_evt[2] + epsilon, (1, .7, .7))

chrono_herve_go   = rel.objects.Chronometer((0,  travel_speed), universe.C, (0, 0, 0),        chrono_period, travel_back_duration,  (.7, .7, 1))
chrono_herve_back = rel.objects.Chronometer((0, -travel_speed), universe.C, U_turn_xyt_Rback, chrono_period, travel_back_duration,  (.7, .7, 1))

universe += chrono_olivier_A
universe += chrono_olivier_B
universe += chrono_olivier_C
universe += chrono_herve_go
universe += chrono_herve_back

universe += start_evts
universe += turn_back_evts
universe += end_evts

start_evts.slice_cross_radius     = .5
turn_back_evts.slice_cross_radius = .5
end_evts.slice_cross_radius       = .5

view_mode = 'olivier'
herve_speed = (0, travel_speed)


def set_view_at_start(t):
    global herve_speed
    herve_speed = (0, travel_speed)
    if view_mode == 'herve':
        universe.set_view_speed(herve_speed)
    
def set_view_at_U_turn(t):
    global herve_speed
    herve_speed = (0, -travel_speed)
    if view_mode == 'herve':
        universe.set_view_speed(herve_speed)
        universe.set_date(U_turn_xyt_Rback[2])
    
def set_view_at_end(t):
    global herve_speed
    herve_speed = (0, 0)
    if view_mode == 'herve':
        universe.set_view_speed(None)
        universe.set_date(2 * turn_back_date_R0)
    
universe += rel.objects.Notifier(None,              universe.C, (0, 0,                     0), set_view_at_start )
universe += rel.objects.Notifier((0, travel_speed), universe.C, (0, 0, travel_back_duration ), set_view_at_U_turn)
universe += rel.objects.Notifier(None,              universe.C, (0, 0, 2 * turn_back_date_R0), set_view_at_end   )


def on_change_view():
    global view_mode
    if view_mode == 'olivier':
        view_mode = 'herve'
        universe.set_view_speed(herve_speed)
    else:
        view_mode = 'olivier'
        universe.set_view_speed(None)

def set_herve_view():
    global view_mode
    view_mode = 'herve'
    universe.set_view_speed(herve_speed)
    
def set_olivier_view():
    global view_mode
    view_mode = 'olivier'
    universe.set_view_speed(None)

def set_upship_view():
    global view_mode
    view_mode = 'up'
    universe.set_view_speed((0, travel_speed))

def set_downship_view():
    global view_mode
    view_mode = 'down'
    universe.set_view_speed((0, -travel_speed))

universe.on_key_pressed('h', set_herve_view)
universe.on_key_pressed('o', set_olivier_view)
universe.on_key_pressed('u', set_upship_view)
universe.on_key_pressed('d', set_downship_view)
print("press h to view from Hervé's reference frame.")
print("press o to view from Olivier's reference frame.")
print("press u to view from up spaceship reference frame.")
print("press d to view from down spaceship reference frame.")
print()

# Let us compare the proper times of olivier and herve.
print()
print()
nb_ticks_olivier = len(chrono_olivier_A.events) + len(chrono_olivier_B.events) + len(chrono_olivier_C.events)
nb_ticks_herve = len(chrono_herve_go.events) + len(chrono_herve_back.events) - 1
text = 'Olivier, staying on the ground, has experienced {} proper chronometer\nticks while Hervé, travelling, has experienced only {} of them. At the\nend, Olivier is {} seconds older than Hervé. Hervé has juped {} ticks\nin the future of Olivier at U-turn.'
print(text.format(nb_ticks_olivier, nb_ticks_herve, (nb_ticks_olivier - nb_ticks_herve) * chrono_period,  len(chrono_olivier_B.events)))
print()
print()

universe.run()
