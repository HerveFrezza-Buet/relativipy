import numpy as np
from . import spacetime

def direct(speed, C) :
    """
    speed = np.array([vx, vy]) : the speed of the moving referential.
    C                          : the speed of light.
    
    returns L such as np.dot(L, np.array([x, y, ct]).T).T = np.array([x', y', ct'])
            where [x', y', ct'] are the coordinates in the moving referential.
    """
    
    v2 = np.dot(speed, speed)
    if v2 == 0 :
        return np.eye(3, 3)
    vxx     = speed[0]**2 / v2
    vyy     = speed[1]**2 / v2
    vxy     = speed[0] * speed[1] / v2
    gamma   = 1/np.sqrt(1 - v2/C**2)
    gamma_1 = gamma - 1
    gvxc    = -gamma * speed[0] / C
    gvyc    = -gamma * speed[1] / C
    return np.array([[1 + gamma_1 * vxx,     gamma_1 * vxy,  gvxc],
                     [    gamma_1 * vxy, 1 + gamma_1 * vyy,  gvyc],
                     [             gvxc,              gvyc, gamma]])

def inverse(speed, C) :
    return direct(-speed, C)

def to_spacetime(speed, C, events) :
    """
    events = np.array([[x1, y1, t1], [x2, y2, t2], ...]) expressed in a moving referential.
    C                          : the speed of light.
    speed = np.array([vx, vy]) : The speed (relative to R0) of the referential where 
                                 the events are defined. Provide None (or np.zeros(2)) 
                                 for defining the events in the R0 referential.
    Returns : the events, expressed in R0 referential, with ct as a time coordinate
              (while argulent has t times).
    """
    e_ct = events * np.array([1, 1, C])
    if speed is None:
        return e_ct
    return spacetime.transform(inverse(speed, C), e_ct)
