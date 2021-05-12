import numpy as np
from . import lorentz

import sys

class Thing:
    def __init__(self, speed):
        if speed is not None:
            self.speed = np.array([speed[0], speed[1]], dtype=np.float32)
        else:
            self.speed = None
    
class ColoredThing(Thing) : 
    def __init__(self, speed, color):
        Thing.__init__(self, speed)
        self.color = color

class Persistant(ColoredThing) :
    def __init__(self, speed, C, time_interval, xy_points, color):
        ColoredThing.__init__(self, speed, color)
        
        tmin, tmax = time_interval
        if tmin is None :
            tmin = -1000
        if tmax is None :
            tmax = 1000

        start = np.hstack((xy_points, np.full((len(xy_points), 1), tmin)))
        end   = np.hstack((xy_points, np.full((len(xy_points), 1), tmax)))

        start = lorentz.to_spacetime(self.speed, C, start)
        end   = lorentz.to_spacetime(self.speed, C, end)

        self.segments = np.hstack((start, end)).reshape((len(start), 2, 3))
        self.nb_segments = len(self.segments)
        
        nb_vertices = 2 * len(self.segments)
        self.line_vertices = self.segments.reshape(nb_vertices, 3)
    
        self.lines_program = None
            
    def build_programs(self):
        
        self.lines_program['color']    = self.color[0], self.color[1], self.color[2], 1
        self.lines_program['pos']      = self.line_vertices


        
class Prism(Persistant):
    def __init__(self, speed, C, time_interval, xy_points, color):
        Persistant.__init__(self, speed, C, time_interval, xy_points, color)
        

        l = [[a, b, d, c] for (a, b), (c, d)  in zip(self.segments[:-1], self.segments[1:])]
        nb_vertices = 4 * len(l)
        self.quad_vertices = np.array(l).reshape(nb_vertices, 3)

        
        self.max_nb_slice_line_vertices = 2*(self.nb_segments+4)
        
        self.quads_program = None
        self.s_slice_program = None
        self.t_slice_program = None
        

    def build_programs(self):
        Persistant.build_programs(self)
        
        self.quads_program['color']    = self.color[0], self.color[1], self.color[2], .25
        self.quads_program['pos']      = self.quad_vertices

        self.s_slice_program['color']  = self.color[0], self.color[1], self.color[2], 1
        self.s_slice_program['point']  = np.zeros((self.max_nb_slice_line_vertices, 2), dtype=np.float32)
        self.s_slice_program['scale']  = 1.0
        self.s_slice_program['trans']  = (0., 0.)
        
        self.t_slice_program['color']  = self.color[0], self.color[1], self.color[2], 1
        self.t_slice_program['point']  = np.zeros((self.max_nb_slice_line_vertices, 2), dtype=np.float32)

    def current_slice(self, L, C, ct) :
        buf = np.zeros((self.max_nb_slice_line_vertices, 2), dtype=np.float32)
        segments = self.segments.reshape((2 * self.nb_segments, 3))
        segments = lorentz.transform(L, segments).reshape(self.segments.shape)
        s = lorentz.ct_slice_of_quads(segments, ct)
        if s is not None:
            buf[0:len(s)] = s
        return buf


class Events(ColoredThing) :
    def __init__(self, speed, C, xyt_points, color):
        ColoredThing.__init__(self, speed, color)
        
        self.spot_duration = .30 # second
        self.cross_radius  = .05
        self.slice_cross_radius  = .1
    
        self.events = lorentz.to_spacetime(self.speed, C, xyt_points)
        self.nb_line_crosses        = 6 * len(self.events)
        self.nb_line_sliced_crosses = 4 * len(self.events)

        self.s_cross_program = None
        self.s_slice_cross_program = None
        self.t_slice_cross_program = None
        
    def build_programs(self):
        self.s_cross_program['color'] = self.color[0], self.color[1], self.color[2], 1
        self.s_cross_program['pos']   = np.zeros((self.nb_line_crosses, 3), dtype=np.float32)
        self.s_cross_program['scale'] = 1.0
        self.s_cross_program['trans'] = (0., 0.)
        self.s_slice_cross_program['color'] = self.color[0], self.color[1], self.color[2], 1
        self.s_slice_cross_program['pos'] = np.zeros((self.nb_line_sliced_crosses, 3), dtype=np.float32)
        self.s_slice_cross_program['scale'] = 1.0
        self.s_slice_cross_program['trans'] = (0., 0.)
        
        self.t_slice_cross_program['color'] = self.color[0], self.color[1], self.color[2], 1
        self.t_slice_cross_program['pos'] = np.zeros((self.nb_line_sliced_crosses, 3), dtype=np.float32)

    def current_events(self, L, C) :
        centers = lorentz.transform(L, self.events)
        d  = self.cross_radius
        dx = np.array([1, 0, 0]) * d
        dy = np.array([0, 1, 0]) * d
        dt = np.array([0, 0, 1]) * d
        return np.hstack((centers + dx, centers - dx, centers - dy, centers + dy, centers - dt, centers + dt)).reshape(self.nb_line_crosses, 3)

    def current_slice(self, L, C, ct) :
        buf = np.zeros((self.nb_line_sliced_crosses, 3), dtype=np.float32)
        centers = lorentz.transform(L, self.events)
        rho = self.spot_duration*C
        select = np.logical_and(ct >= centers[...,2], centers[...,2] >= ct-rho)
        centers = centers[select]
        nb_centers = len(centers)
        if nb_centers > 0 :
            crosses_radius = ((centers[..., 2] + (rho - ct)) * (self.slice_cross_radius/rho)).reshape((nb_centers, 1))
            dx = crosses_radius * np.array([1, 0, 0])
            dy = crosses_radius * np.array([0, 1, 0])
            size = 4 * len(centers)
            data = np.hstack((centers - dx, centers + dx, centers - dy, centers + dy)).reshape(size, 3)
            buf[0:size] = data
        return buf
        
class Chronometer(Events):
    def __init__(self, speed, C, start_event, tick_period, duration, color):
        n = 1
        t = start_event[2]
        times = [t]
        t = times[0] + tick_period
        end = times[0] + duration
        while t <= end :
            times.append(t)
            n += 1
            t = times[0] + n * tick_period
        xyt_points = np.array([[start_event[0], start_event[1], t] for t in times])
        Events.__init__(self, speed, C, xyt_points, color)

class Points(Persistant):
    def __init__(self, speed, C, time_interval, xy_points, color):
        Persistant.__init__(self, speed, C, time_interval, xy_points, color)
        self.nb_vertices_sliced_crosses = 4*self.nb_segments
        
        self.cross_radius  = .05
        
        self.s_slice_cross_program = None
        self.t_slice_cross_program = None
        
    def build_programs(self):
        Persistant.build_programs(self)
        
        self.s_slice_cross_program['color'] = self.color[0], self.color[1], self.color[2], 1
        self.s_slice_cross_program['pos'] = np.zeros((self.nb_vertices_sliced_crosses, 3), dtype=np.float32)
        self.s_slice_cross_program['scale'] = 1.0
        self.s_slice_cross_program['trans'] = (0., 0.)
        
        self.t_slice_cross_program['color'] = self.color[0], self.color[1], self.color[2], 1
        self.t_slice_cross_program['pos'] = np.zeros((self.nb_vertices_sliced_crosses, 3), dtype=np.float32)

    def current_slice(self, L, C, ct) :
        buf = np.zeros((self.nb_vertices_sliced_crosses, 3), dtype=np.float32)
        segments = self.segments.reshape((2 * self.nb_segments, 3))
        segments = lorentz.transform(L, segments).reshape(self.segments.shape)
        centers = lorentz.slice_points_of_segments(ct, segments)
        if len(centers) > 0 :
            dx = np.array([self.cross_radius, 0, 0])
            dy = np.array([0, self.cross_radius, 0])
            size = 4 * len(centers)
            data = np.hstack((centers - dx, centers + dx, centers - dy, centers + dy)).reshape(size, 3)
            buf[0:size] = data
        return buf

class Notifier(Thing):
    def __init__(self, speed, C, xyt_event, callback):
        Thing.__init__(self, speed)
        self.event = lorentz.to_spacetime(self.speed, C, np.array([xyt_event]))
        self.cb = callback
        self.not_called = True
        
    def ack(self):
        self.not_called = True

    def notify(self, L, ct):
        if self.not_called:
            t = lorentz.transform(L, self.event)[0][2]
            if t <= ct:
                self.cb(t)
                self.not_called = False
    

light_cone_pie_nb = 50
light_cone_circle_2D = np.array([[np.sin(t), np.cos(t)] for t in np.linspace(0, 2*np.pi, light_cone_pie_nb)])
light_cone_circle_3D = np.array([[np.sin(t), np.cos(t), 0] for t in np.linspace(0, 2*np.pi, light_cone_pie_nb)])
class LightCone :
    def __init__(self, C, start, end, color):
        self.color = color
        self.bounds = np.array([start, end])
        self.nb_vertices = 1 + light_cone_pie_nb
        self.slice_size  = light_cone_pie_nb

        self.fan_program     = None
        self.s_slice_program = None
        self.t_slice_program = None
        
    def build_programs(self):
        self.fan_program['color'] = self.color[0], self.color[1], self.color[2], .25
        self.fan_program['pos']   = np.zeros((self.nb_vertices, 3), dtype=np.float32)
        self.fan_program['scale'] = 1.0
        self.fan_program['trans'] = (0., 0.)
        
        self.s_slice_program['color'] = self.color[0], self.color[1], self.color[2], 1
        self.s_slice_program['pos']   = np.zeros((self.slice_size, 3), dtype=np.float32)
        self.s_slice_program['scale'] = 1.0
        self.s_slice_program['trans'] = (0., 0.)
        
        self.t_slice_program['color'] = self.color[0], self.color[1], self.color[2], 1
        self.t_slice_program['pos']   = np.zeros((self.slice_size, 3), dtype=np.float32)

    def current_cone(self, L, C):
        start, end = lorentz.transform(L, self.bounds)
        radius = C*(end[2] - start[2])
        buf = np.zeros((self.nb_vertices, 3), dtype=np.float32)
        buf[0]  = start
        start[2] = end[2]
        buf[1:] = start + radius * light_cone_circle_3D
        return buf
    
    def current_slice(self, L, C, ct):
        buf = np.zeros((self.slice_size, 3), dtype=np.float32)
        start, end = lorentz.transform(L, self.bounds)
        if start[2] <= ct <= end[2]:
            radius   = C*(ct - start[2])
            start[2] = ct
            buf[...] = start + radius * light_cone_circle_3D
        return buf
        
