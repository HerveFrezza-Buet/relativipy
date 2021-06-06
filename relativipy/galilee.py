import numpy as np

def direct(speed, C) :
    """
    speed = np.array([vx, vy]) : the speed of the moving referential.
    C                          : the speed of light.
    
    returns G such as np.dot(G, np.array([x, y, ct]).T).T = np.array([x', y', ct'])
            where [x', y', ct'] are the coordinates in the moving referential.
    """
    
    return np.array([[1, 0, -speed[0]/C],
                     [0, 1, -speed[1]/C],
                     [0, 0,           1])

def inverse(speed, C) :
    return direct(-speed, C)

def transform(G, ct_events) :
    """
    G is a Galilee matrix
    ct_events = np.array([[x1, y1, ct1], [x2, y2, ct2], ...]) expressed in a moving referential.
    C                          : the speed of light.
    """
    return np.dot(G, ct_events.T).T

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
    return transform(inverse(speed, C), e_ct)
