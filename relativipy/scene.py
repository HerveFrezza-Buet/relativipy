import numpy as np
from glumpy import app, gloo, gl
from glumpy.transforms import Trackball, Position, Translate, OrthographicProjection, PanZoom

from . import objects
from . import lorentz

class Shader():
    def __init__(self, vertex, fragment):
        self.vertex   = vertex
        self.fragment = fragment
        
class Universe:
    def draw_time(self):
        self.window.clear(color=(1,1,1,1))
        self.set_programs_data()
        
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glLineWidth(1.0)
        if self.axes_origin is not None:
            self.t_axes.draw(gl.GL_LINES)
        gl.glLineWidth(3.0)
        for p in self.prisms :
            p.t_slice_program.draw(gl.GL_LINES)
        for e in self.events :
            e.t_slice_cross_program.draw(gl.GL_LINES)
        for p in self.points :
            p.t_slice_cross_program.draw(gl.GL_LINES)
        for l in self.lights :
            l.t_slice_program.draw(gl.GL_LINE_STRIP)
        
    def draw_spacetime(self):
        self.window.clear(color=self.bgcolor)

        self.set_programs_data()

        if self.screen_mode:
            # We draw prisms, writing the z-buffer but not the frame buffer.
            gl.glEnable(gl.GL_DEPTH_TEST)
            gl.glDepthMask(gl.GL_TRUE)
            gl.glColorMask(gl.GL_FALSE, gl.GL_FALSE, gl.GL_FALSE, gl.GL_FALSE)
            for p in self.prisms:
                p.quads_program.draw(gl.GL_QUADS)
            for l in self.lights:
                l.fan_program.draw(gl.GL_TRIANGLE_FAN)
            gl.glColorMask(gl.GL_TRUE, gl.GL_TRUE, gl.GL_TRUE, gl.GL_TRUE)

        
            # Then, we plot the screen for the first time.
            gl.glEnable(gl.GL_BLEND)
            self.screen.draw(gl.GL_QUADS)
            
            # We restart z-buffer.
            gl.glClear(gl.GL_DEPTH_BUFFER_BIT)
            
        # Mode for drawing opaque
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glDepthMask(gl.GL_TRUE)
        gl.glDisable(gl.GL_BLEND)
    
        # Draw opaque
        gl.glLineWidth(1.0)
        self.frame.draw(gl.GL_LINES)
        if self.show_prism_lines:
            for p in self.persistants :
                p.lines_program.draw(gl.GL_LINES)
        for e in self.events :
            e.s_cross_program.draw(gl.GL_LINES)
        gl.glEnable(gl.GL_POLYGON_OFFSET_FILL)
        gl.glLineWidth(3.0)
        if self.screen_mode and self.axes_origin is not None:
            self.s_axes.draw(gl.GL_LINES)
        for p in self.prisms :
            p.s_slice_program.draw(gl.GL_LINES)
        for l in self.lights :
            l.s_slice_program.draw(gl.GL_LINE_STRIP)
        for e in self.events :
            e.s_slice_cross_program.draw(gl.GL_LINES)
        for p in self.points :
            p.s_slice_cross_program.draw(gl.GL_LINES)
        gl.glDisable(gl.GL_POLYGON_OFFSET_FILL)
        
        # mode for drawing transparent
        gl.glDepthMask(gl.GL_FALSE)
        gl.glEnable(gl.GL_BLEND)
        
        # Draw transparent
        for p in self.prisms:
            p.quads_program.draw(gl.GL_QUADS)
        for l in self.lights:
            l.fan_program.draw(gl.GL_TRIANGLE_FAN)
        if self.screen_mode:
            self.screen.draw(gl.GL_QUADS)
        
        # end of drawing transparent... required.
        gl.glDepthMask(gl.GL_TRUE)
        
    def on_draw(self, dt):

        self.ct += self.C * dt; 
        if self.spacetime_mode:
            self.draw_spacetime()
        else:
            self.draw_time()
            

    def toggle_view_mode(self):
        self.spacetime_mode = not self.spacetime_mode
        
    def toggle_screen_mode(self):
        self.screen_mode = not self.screen_mode
        
    def __init__(self, screen_size = (4., 3.), width=640, height=480, color=(0.30, 0.30, 0.35, 1.00)):

        self.spacetime_mode   = True
        self.screen_mode      = True
        self.axes_origin      = (0, 0)
        self.show_prism_lines = True
        
        self.bgcolor = color
        self.scale          = 1.
        self.trans          = (0., 0.)
        self.C      = 1
        self.ct     = 0
        self.t_max  = 5
        self.screen_size = screen_size
        self.prisms = []
        self.points = []
        self.events = []
        self.lights = []
        self.notifiers = []
        self.persistants = []
        self.restart_callbacks = []
        self.s_shaders = {}
        self.t_shaders = {}
        self.make_shaders()
        self.lorentz       = np.eye(3,3)
        self.current_speed = np.array([0., 0], dtype=np.float32)

        self.adjust_t_max = False
        self.speed = np.array([0., 0], dtype=np.float32)

        self.key_pressed_cb = {}

        print()
        print()
        print("Press 't' to change the view mode")
        print("Press 's' to toggle the screen instanciation in the 3D view")
        print()
        self.on_key_pressed('t', self.toggle_view_mode)
        self.on_key_pressed('s', self.toggle_screen_mode)
        
        window = app.Window(width=width, height=height, color=color)
        self.window = window
        
        @window.event
        def on_resize(width, height):
            self.on_resize(width, height)
            
        @window.event
        def on_character(symbol):
            if symbol in self.key_pressed_cb :
                for cb in self.key_pressed_cb[symbol]:
                    cb()
            else:
                print('Key "{}" is unbound.'.format(symbol))
            
        @window.event
        def on_draw(dt):
            self.on_draw(dt)
            
        @window.event
        def on_init():
            gl.glEnable(gl.GL_DEPTH_TEST)
            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
            gl.glPolygonOffset(3, 3)
            gl.glEnable(gl.GL_LINE_SMOOTH)

    def on_resize(self, width, height):
        self.trans = (.5*width, .5*height)
        self.scale = min(width/self.screen_size[0], height/self.screen_size[1])
        
    def on_key_pressed(self, symbol, cb):
        if symbol in self.key_pressed_cb:
            self.key_pressed_cb[symbol].append(cb)
        else:
            self.key_pressed_cb[symbol] = [cb]

    def on_restart(self, cb):
        self.restart_callbacks.append(cb)
        

    def make_shaders(self):
        self.make_frame_shader()
        self.make_screen_shader()
        self.make_prism_shader()
        self.make_slice_shader()
        self.make_events_shader()

    def make_frame(self):
        self.frame = gloo.Program(self.s_shaders['frame'].vertex, self.s_shaders['frame'].fragment, count=24)
        w = self.screen_size[0] * .5
        h = self.screen_size[1] * .5
        self.frame['pos'] = np.array([[ -w, -h, 0.], [ -w, -h, 1.],
                                      [  w, -h, 0.], [  w, -h, 1.],
                                      [ -w,  h, 0.], [ -w,  h, 1.],
                                      [  w,  h, 0.], [  w,  h, 1.],
                                      [ -w, -h, 0.], [  w, -h, 0.],
                                      [ -w, -h, 1.], [  w, -h, 1.],
                                      [ -w,  h, 0.], [  w,  h, 0.],
                                      [ -w,  h, 1.], [  w,  h, 1.],
                                      [ -w, -h, 0.], [ -w,  h, 0.],
                                      [ -w, -h, 1.], [ -w,  h, 1.],
                                      [  w, -h, 0.], [  w,  h, 0.],
                                      [  w, -h, 1.], [  w,  h, 1.]])
        self.frame['color'] = 0, 0, 0, 1
        
    def make_screen(self):
        self.screen = gloo.Program(self.s_shaders['screen'].vertex, self.s_shaders['screen'].fragment, count=4)
        w = self.screen_size[0] * .5
        h = self.screen_size[1] * .5
        self.screen['pos']   = np.array([[ -w, -h], [w, -h], [w, h], [-w, h]])
        self.screen['color'] = 1, 1, 1, .75
        self.screen['scale'] = 1.0
        self.screen['trans'] = (0., 0.)
        
    def make_axes(self):
        self.s_axes = gloo.Program(self.s_shaders['screen'].vertex, self.s_shaders['screen'].fragment, count=4)
        self.t_axes = gloo.Program(self.t_shaders['screen'].vertex, self.t_shaders['screen'].fragment, count=4)
        w = self.screen_size[0] * .5
        h = self.screen_size[1] * .5
        vertices = np.array([[-w, 0], [w, 0], [0, -h], [0, h]])
        self.s_axes['pos']    = vertices
        self.s_axes['color']  = .3, .3, .75, 1
        self.s_axes['scale']  = 1.0
        self.s_axes['trans']  = (0., 0.)
        self.t_axes['pos']    = vertices
        self.t_axes['color']  = .8, .8, 1, 1
        self.t_axes['ct']     = 0
        self.t_axes['ct_max'] = 0

    def force_view_speed(self, speed):
        if speed is not None:
            self.speed = np.array([speed[0], speed[1]], dtype=np.float32)
        else:
            self.speed = np.array([0., 0], dtype=np.float32)
        self.current_speed = self.speed
        
    def set_view_speed(self, speed):
        if speed is not None:
            self.speed = np.array([speed[0], speed[1]], dtype=np.float32)
        else:
            self.speed = np.array([0., 0], dtype=np.float32)
    def __iadd__(self, obj):
        if isinstance(obj, objects.Prism):
            self.add_persistant(obj) # This first, from mother to terminal classes.
            self.add_prism(obj)
        elif isinstance(obj, objects.Points):
            self.add_persistant(obj) # This first, from mother to terminal classes.
            self.add_points(obj)
        elif isinstance(obj, objects.Events):
            self.add_events(obj)
        elif isinstance(obj, objects.LightCone):
            self.add_light(obj)
        elif isinstance(obj, objects.Notifier):
            self.add_notifier(obj)
        else:
            print()
            print('WARNING : Cannot add objet of type {}'.format(type(obj)))
            print()
        return self

    def add_notifier(self, obj):
        self.notifiers.append(obj)
        return obj
        
    def add_light(self, light):
        light.fan_program = gloo.Program(self.s_shaders['events'].vertex, self.s_shaders['events'].fragment, count=light.nb_vertices)
        light.s_slice_program = gloo.Program(self.s_shaders['events'].vertex, self.s_shaders['events'].fragment, count=light.slice_size)
        light.t_slice_program = gloo.Program(self.s_shaders['events'].vertex, self.s_shaders['events'].fragment, count=light.slice_size)
        light.build_programs()
        self.lights.append(light)
        return light

    def add_persistant(self, persistant):
        persistant.lines_program   = gloo.Program(self.s_shaders['prism'].vertex, self.s_shaders['prism'].fragment)
        self.persistants.append(persistant)
        return persistant
        
    def add_points(self, pts):
        pts.s_slice_cross_program = gloo.Program(self.s_shaders['events'].vertex, self.s_shaders['events'].fragment, count=pts.nb_vertices_sliced_crosses)     
        pts.t_slice_cross_program = gloo.Program(self.t_shaders['events'].vertex, self.t_shaders['events'].fragment, count=pts.nb_vertices_sliced_crosses)      
        pts.build_programs()
        self.points.append(pts)
        return pts
    
    def add_prism(self, prism):
        prism.quads_program   = gloo.Program(self.s_shaders['prism'].vertex, self.s_shaders['prism'].fragment)
        prism.s_slice_program = gloo.Program(self.s_shaders['slice'].vertex, self.s_shaders['slice'].fragment, count=prism.max_nb_slice_line_vertices)
        prism.t_slice_program = gloo.Program(self.t_shaders['slice'].vertex, self.t_shaders['slice'].fragment, count=prism.max_nb_slice_line_vertices)        
        prism.build_programs()
        self.prisms.append(prism)
        return prism

    def add_events(self, event):
        event.s_cross_program = gloo.Program(self.s_shaders['events'].vertex, self.s_shaders['events'].fragment, count=event.nb_line_crosses)     
        event.s_slice_cross_program = gloo.Program(self.s_shaders['events'].vertex, self.s_shaders['events'].fragment, count=event.nb_line_sliced_crosses)     
        event.t_slice_cross_program = gloo.Program(self.t_shaders['events'].vertex, self.t_shaders['events'].fragment, count=event.nb_line_sliced_crosses)      
        event.build_programs()
        self.events.append(event)
        return event
    
        
    def run(self):
        self.make_frame()
        self.make_screen()
        self.make_axes()

        trackball = Trackball(Position("position"))
        self.spacetime_transform = trackball

        self.time_transform = OrthographicProjection(Position("position"))


        self.set_time_transforms()
        self.set_spacetime_transforms()
        trackball.phi   = -5
        trackball.theta = -30
        trackball.distance = 15
        trackball.zoom  =  35
        self.window.attach(self.time_transform)
        self.window.attach(self.spacetime_transform)
        
        for cb in self.restart_callbacks:
            cb()
        app.run()

    def set_time_transforms(self):
        self.time_transform = OrthographicProjection(Position("position"))
        self.t_axes['transform']                 = self.time_transform
        for p in self.prisms:
            p.t_slice_program['transform']       = self.time_transform
        for e in self.events:
            e.t_slice_cross_program['transform'] = self.time_transform
        for p in self.points:
            p.t_slice_cross_program['transform'] = self.time_transform
        for l in self.lights:
            l.t_slice_program['transform']       = self.time_transform
        
    def set_spacetime_transforms(self):
        self.frame['transform']                  = self.spacetime_transform
        self.screen['transform']                 = self.spacetime_transform
        self.s_axes['transform']                 = self.spacetime_transform
        for p in self.persistants:
            p.lines_program['transform']         = self.spacetime_transform
        for p in self.prisms:
            p.quads_program['transform']         = self.spacetime_transform
            p.s_slice_program['transform']       = self.spacetime_transform
        for e in self.events:
            e.s_cross_program['transform']       = self.spacetime_transform
            e.s_slice_cross_program['transform'] = self.spacetime_transform
        for p in self.points:
            p.s_slice_cross_program['transform'] = self.spacetime_transform
        for l in self.lights:
            l.fan_program['transform']           = self.spacetime_transform
            l.s_slice_program['transform']       = self.spacetime_transform
        
    def set_programs_data(self):
        w = self.screen_size[0] * .5
        h = self.screen_size[1] * .5

        if self.axes_origin is not None:
            vertices = np.array([[-w, self.axes_origin[1]], [w, self.axes_origin[1]], [self.axes_origin[0], -h], [self.axes_origin[0], h]])
            self.s_axes['pos'] = vertices
            self.t_axes['pos'] = vertices
        
        alpha = .1
        self.current_speed += alpha * (self.speed - self.current_speed)
        self.lorentz    = lorentz.direct(self.current_speed, self.C)

        if self.adjust_t_max:
            self.ct_max = lorentz.transform(self.lorentz, np.array([[0, 0, self.C * self.t_max]]))[0][2]
        else:
            self.ct_max = self.C * self.t_max
            
        if self.ct > self.ct_max:
            self.ct = 0
            for n in self.notifiers:
                n.ack()
            for cb in self.restart_callbacks:
                cb()
            
            
        self.screen['ct']      = self.ct
        self.screen['ct_max']  = self.ct_max
        self.frame['ct_max']   = self.ct_max

        L  = self.lorentz.T

            
        for n in self.notifiers:
            n.notify(L, self.ct)
            
        for p in self.prisms :
            p.quads_program['half_screen_size'] = w, h
            p.quads_program['ct_max']           = self.ct_max
            p.quads_program['lorentz']          = L

        if self.spacetime_mode:
            self.set_spacetime_programs_data(w, h, L)
        else:
            self.set_time_programs_data(w, h, L)

    def set_spacetime_programs_data(self, w, h, L):
        self.s_axes['ct']      = self.ct
        self.s_axes['ct_max']  = self.ct_max

        if self.show_prism_lines:
            for p in self.persistants :
                p.lines_program['half_screen_size'] = w, h
                p.lines_program['ct_max']           = self.ct_max
                p.lines_program['lorentz']          = L
            
        for p in self.prisms :
            p.s_slice_program['half_screen_size'] = w, h
            p.s_slice_program['ct_max']           = self.ct_max
            p.s_slice_program['ct']               = self.ct
            p.s_slice_program['point']            = p.current_slice(L, self.C, self.ct)
            
        for e in self.events :
            e.s_cross_program['half_screen_size']       = w, h
            e.s_cross_program['ct_max']                 = self.ct_max
            e.s_cross_program['pos']                    = e.current_events(L, self.C)
            e.s_slice_cross_program['half_screen_size'] = w, h
            e.s_slice_cross_program['ct_max']           = self.ct_max
            e.s_slice_cross_program['pos']              = e.current_slice(L, self.C, self.ct)
            
        for p in self.points :
            p.s_slice_cross_program['half_screen_size'] = w, h
            p.s_slice_cross_program['ct_max']           = self.ct_max
            p.s_slice_cross_program['pos']              = p.current_slice(L, self.C, self.ct)
            
        for l in self.lights :
            l.fan_program['half_screen_size']     = w, h
            l.fan_program['ct_max']               = self.ct_max
            l.fan_program['pos']                  = l.current_cone(L, self.C)
            l.s_slice_program['half_screen_size'] = w, h
            l.s_slice_program['ct_max']           = self.ct_max
            l.s_slice_program['pos']              = l.current_slice(L, self.C, self.ct)

    def set_time_programs_data(self, w, h, L):
        self.t_axes['scale'] = self.scale
        self.t_axes['trans'] = self.trans
        
        for p in self.prisms :
            p.t_slice_program['half_screen_size'] = w, h
            p.t_slice_program['scale']            = self.scale
            p.t_slice_program['trans']            = self.trans
            p.t_slice_program['ct']               = self.ct
            p.t_slice_program['point']            = p.current_slice(L, self.C, self.ct)
            
        for e in self.events :
            e.t_slice_cross_program['half_screen_size'] = w, h
            e.t_slice_cross_program['scale']            = self.scale
            e.t_slice_cross_program['trans']            = self.trans
            e.t_slice_cross_program['ct_max']           = self.ct_max
            e.t_slice_cross_program['pos']              = e.current_slice(L, self.C, self.ct)
            
        for p in self.points :
            p.t_slice_cross_program['half_screen_size'] = w, h
            p.t_slice_cross_program['scale']            = self.scale
            p.t_slice_cross_program['trans']            = self.trans
            p.t_slice_cross_program['ct_max']           = self.ct_max
            p.t_slice_cross_program['pos']              = p.current_slice(L, self.C, self.ct)
            
        for l in self.lights :
            l.t_slice_program['half_screen_size'] = w, h
            l.t_slice_program['scale']            = self.scale
            l.t_slice_program['trans']            = self.trans
            l.t_slice_program['ct_max']           = self.ct_max
            l.t_slice_program['pos']              = l.current_slice(L, self.C, self.ct)
        
    def make_frame_shader(self):
        vertex = """
        uniform float ct_max;
        attribute vec3 pos;
        void main()
        {
            vec3 position = vec3(pos.x, pos.y, ct_max * pos.z - ct_max/2);
            gl_Position = <transform>;
        } 
        """
        fragment = """
        uniform vec4 color;
        void main() {
            gl_FragColor = color;
        }"""
        self.s_shaders['frame'] = Shader(vertex, fragment)
        
    def make_screen_shader(self):
        vertex = """
        uniform float ct_max;
        uniform float ct;
        uniform vec2 trans;
        uniform float scale;
        attribute vec2 pos;
        void main()
        {
            vec3 position = vec3(pos.x, pos.y, ct - ct_max/2)*scale + vec3(trans, 0); 
            gl_Position = <transform>;
        } 
        """
        fragment = """
        uniform vec4 color;
        void main() {
            gl_FragColor = color;
        }"""
        self.s_shaders['screen'] = Shader(vertex, fragment)
        self.t_shaders['screen'] = Shader(vertex, fragment)
        
    def make_prism_shader(self):
        vertex = """
        uniform float ct_max;
        uniform vec2 half_screen_size;
        uniform mat3 lorentz;
        attribute vec3 pos;
        varying   vec3 p;
        void main()
        {
            p = lorentz * pos;
            vec3 position = vec3(p.x, p.y, p.z - ct_max/2);
            gl_Position = <transform>;
        } 
        """
        fragment = """
        uniform float ct_max;
        uniform vec4 color;
        uniform vec2 half_screen_size;
        varying   vec3 p;
        void main() {
        if(p.x < -half_screen_size.x) discard;
        if(p.x >  half_screen_size.x) discard;
        if(p.y < -half_screen_size.y) discard;
        if(p.y >  half_screen_size.y) discard;
        if(p.z <  0                 ) discard;
        if(p.z >  ct_max            ) discard;
            gl_FragColor = color;
        }"""
        self.s_shaders['prism'] = Shader(vertex, fragment)
        
    def make_slice_shader(self):
        vertex = """
        attribute vec2 point;
        uniform float ct_max;
        uniform float ct;
        uniform vec2 trans;
        uniform float scale;
        uniform vec2 half_screen_size;
        varying   vec2 p;
        void main()
        {
            vec3 position = vec3(point*scale + trans, ct - ct_max/2); 
            p = point;
            gl_Position = <transform>;
        } 
        """
        fragment = """
        uniform vec4 color;
        uniform vec2 half_screen_size;
        varying   vec2 p;
        void main() {
        if(p.x < -half_screen_size.x) discard;
        if(p.x >  half_screen_size.x) discard;
        if(p.y < -half_screen_size.y) discard;
        if(p.y >  half_screen_size.y) discard;
        gl_FragColor = color;
        }"""
        self.s_shaders['slice'] = Shader(vertex, fragment)
        self.t_shaders['slice'] = Shader(vertex, fragment)
        

    def make_events_shader(self):
        vertex = """
        uniform float ct_max;
        uniform vec2 half_screen_size;
        uniform vec2 trans;
        uniform float scale;
        attribute vec3 pos;
        varying   vec3 p;
        void main()
        {
            p = pos;
            vec3 position = vec3(p.xy * scale + trans, p.z - ct_max/2);
            gl_Position = <transform>;
        } 
        """
        fragment = """
        uniform float ct_max;
        uniform vec4 color;
        uniform vec2 half_screen_size;
        varying   vec3 p;
        void main() {
        if(p.x < -half_screen_size.x) discard;
        if(p.x >  half_screen_size.x) discard;
        if(p.y < -half_screen_size.y) discard;
        if(p.y >  half_screen_size.y) discard;
        if(p.z <  0                 ) discard;
        if(p.z >  ct_max            ) discard;
            gl_FragColor = color;
        }"""
        self.s_shaders['events'] = Shader(vertex, fragment)
        self.t_shaders['events'] = Shader(vertex, fragment)
