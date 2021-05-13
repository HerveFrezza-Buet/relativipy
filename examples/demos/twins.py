import relativipy as rel
import numpy as np


universe = rel.scene.Universe(screen_size = (3, 10), width=800, height=450)
universe.spacetime_mode   = False
universe.show_prism_lines = False
universe.t_max            = 10

human_size           = 1
ground_level         = -human_size/2
travel_speed         = universe.C*.9
travel_go_duration   = 2
travel_back_duration = travel_go_duration

universe.axes_origin = (-1, ground_level)

head  = np.array([[np.sin(t), -np.cos(t)] for t in np.linspace(0, 2*np.pi, 11)])
left  = np.array([(-1, 0), (-1, 3), (-1, 2), (-2, 2), (-2, 4)])
right = np.flip((left * np.array([-1, 1])), axis=0)
human = np.vstack((left, head + np.array([0, 5]), right, np.array([left[0]]))) * human_size/6

twin_start_position = (0, ground_level)
twin = human + twin_start_position

herve        = rel.objects.Prism(None,              universe.C, (None, None              ), twin, (1, 0, 0))
olivier_go   = rel.objects.Prism((0, travel_speed), universe.C, (0,    travel_go_duration), twin, (0, 0, 1))

start_evts     = rel.objects.Events(None             , universe.C, np.array([[0, 0,                   0 ]]), (0, 0, 0))
turn_back_evts = rel.objects.Events((0, travel_speed), universe.C, np.array([[0, 0, travel_back_duration]]),  (0, 0, 0))

turn_back_xyct_R0 = turn_back_evts.events
turn_back_date_R0 = turn_back_xyct_R0[0][2] / universe.C

end_evts = rel.objects.Events(None, universe.C, np.array([[0, 0, 2 * turn_back_date_R0]]), (0, 0, 0))

L_R0_to_Rback        = rel.lorentz.direct(np.array([0, -travel_speed]), universe.C)
turn_back_xyct_Rback = rel.lorentz.transform(L_R0_to_Rback, turn_back_xyct_R0)

U_turn_xyt_Rback = turn_back_xyct_Rback[0] * np.array([1, 1, 1/universe.C])
olivier_back = rel.objects.Prism((0, -travel_speed), universe.C, (U_turn_xyt_Rback[2], U_turn_xyt_Rback[2] + travel_back_duration), twin + U_turn_xyt_Rback[:2], (0, 0, 1))

universe += herve
universe += olivier_go
universe += olivier_back

start_xyt_R0 = start_evts.events[0] * np.array([1, 1, 1/universe.C])
universe += rel.objects.Chronometer(None, universe.C, start_xyt_R0, .25, 2 * turn_back_date_R0, (1, .7, .7))
universe += rel.objects.Chronometer((0,  travel_speed), universe.C, (0, 0, 0),        .25, travel_back_duration, (.7, .7, 1))
universe += rel.objects.Chronometer((0, -travel_speed), universe.C, U_turn_xyt_Rback, .25, travel_back_duration, (.7, .7, 1))

universe += start_evts
universe += turn_back_evts
universe += end_evts

start_evts.slice_cross_radius     = .5
turn_back_evts.slice_cross_radius = .5
end_evts.slice_cross_radius       = .5




universe.run()
