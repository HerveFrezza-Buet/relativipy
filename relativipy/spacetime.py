import numpy as np

def transform(M, ct_events) :
    """
    M is a frame transform matrix
    ct_events = np.array([[x1, y1, ct1], [x2, y2, ct2], ...]) expressed in a moving referential.
    C                          : the speed of light.
    """
    return np.dot(M, ct_events.T).T

def ct_section(ct, A, B, Az, Bz) :
    l = (ct - Az)/(Bz - Az)
    l_ = 1 - l
    return [l_ * A[0] + l * B[0], l_ * A[1] + l * B[1]]

    
def slice_points_of_segments(ct, segments) :
    """
    segments [[[x1, y1, ct1], [x2, y2, ct2]], [[,,], [,,]], ...]
    returns [[x1, y1, ct], [x2, y2, ct], ...]
    """
    res = []
    for  A, B in segments:
        Az = A[2]
        Bz = B[2]
        if Az <= ct and ct <= Bz :
            res.append(ct_section(ct, A, B, Az, Bz)+[ct])
    return np.array(res)
    
def slice_lines_of_quad(ct, A, B, C, D) :
    """
    ABDC has to be a flat quad.
    """
    Az = A[2]
    Bz = B[2]
    Cz = C[2]
    Dz = D[2]
    if Az < ct :
        if Bz < ct :
            if Cz < ct :
                if Dz <= ct :    # A(-1) B(-1) C(-1) D(-1) | A(-1) B(-1) C(-1) D( 0)
                    return []
                else :           # A(-1) B(-1) C(-1) D( 1)
                    return [ct_section(ct, B, D, Bz, Dz), ct_section(ct, C, D, Cz, Dz)]
            elif Cz > ct :
                if Dz < ct :    # A(-1) B(-1) C( 1) D(-1)
                    return [ct_section(ct, A, C, Az, Cz), ct_section(ct, C, D, Cz, Dz)]
                elif Dz > ct :  # A(-1) B(-1) C( 1) D( 1)
                    return [ct_section(ct, A, C, Az, Cz), ct_section(ct, B, D, Bz, Dz)]
                else:           # A(-1) B(-1) C( 1) D( 0)
                    return [ct_section(ct, A, C, Az, Cz), [D[0], D[1]]]
            else: 
                if Dz < ct :    # A(-1) B(-1) C( 0) D(-1)
                    return []
                elif Dz > ct :  # A(-1) B(-1) C( 0) D( 1)
                    return [ct_section(ct, B, D, Bz, Dz), [C[0], C[1]]]
                else:           # A(-1) B(-1) C( 0) D( 0)
                    return [[C[0], C[1]], [D[0], D[1]]]
        elif Bz > ct :
            if Cz < ct :
                if Dz < ct :    # A(-1) B( 1) C(-1) D(-1)
                    return [ct_section(ct, A, B, Az, Bz), ct_section(ct, B, D, Bz, Dz)]
                elif Dz > ct :  # A(-1) B( 1) C(-1) D( 1)
                    return [ct_section(ct, A, B, Az, Bz), ct_section(ct, C, D, Cz, Dz)]
                else:           # A(-1) B( 1) C(-1) D( 0)
                    return [ct_section(ct, A, B, Az, Bz), [D[0], D[1]]]
            elif Cz > ct : # A(-1) B( 1) C( 1) D(1)
                return [ct_section(ct, A, B, Az, Bz), ct_section(ct, A, C, Az, Cz)]
            else: # A(-1) B( 1) C( 0) D( 1)
                return [ct_section(ct, A, B, Az, Bz), [C[0], C[1]]]
        else: 
            if Cz < ct :
                if Dz < ct :    # A(-1) B( 0) C(-1) D(-1)
                    return []
                elif Dz > ct :  # A(-1) B( 0) C(-1) D( 1)
                    return [ct_section(ct, C, D, Cz, Dz), [B[0], B[1]]]
                else:           # A(-1) B( 0) C(-1) D( 0)
                    return [[D[0], D[1]], [B[0], B[1]]]
            elif Cz > ct :
                if Dz < ct :    # A(-1) B( 0) C( 1) D(-1) Impossible
                    return []
                elif Dz > ct :  # A(-1) B( 0) C( 1) D( 1)
                    return [ct_section(ct, A, C, Az, Cz), [B[0], B[1]]] 
                else:           # A(-1) B( 0) C( 1) D( 0) Impossible
                    return []
            else: # A(-1) B( 0) C( 0) D( 1)
                return [ct_section(ct, A, C, Az, Cz), ct_section(ct, A, B, Az, Bz)] 
    elif Az > ct :
        if Bz < ct :
            if Cz < ct : # A( 1) B(-1) C(-1) D(-1)
                return [ct_section(ct, A, C, Az, Cz), ct_section(ct, A, B, Az, Bz)] 
            elif Cz > ct :
                if Dz < ct :    # A( 1) B(-1) C( 1) D(-1)
                    return [ct_section(ct, A, B, Az, Bz), ct_section(ct, C, D, Cz, Dz)]
                elif Dz > ct :  # A( 1) B(-1) C( 1) D( 1)
                    return [ct_section(ct, A, B, Az, Bz), ct_section(ct, B, D, Bz, Dz)]
                else:           # A( 1) B(-1) C( 1) D( 0)
                    return [ct_section(ct, A, B, Az, Bz), [D[0], D[1]]]
            else:
                # A( 1) B(-1) C( 0) D(-1)
                # A( 1) B(-1) C( 0) D( 1) or # A( 1) B(-1) C( 0) D( 0) Impossible
                return [ct_section(ct, A, B, Az, Bz), [C[0], C[1]]]
        elif Bz > ct :
            if Cz < ct :
                if Dz < ct :    # A( 1) B( 1) C(-1) D(-1)
                    return [ct_section(ct, A, C, Az, Cz), ct_section(ct, B, D, Bz, Dz)]
                elif Dz > ct :  # A( 1) B( 1) C(-1) D( 1)
                    return [ct_section(ct, A, C, Az, Cz), ct_section(ct, C, D, Cz, Dz)]
                else:           # A( 1) B( 1) C(-1) D( 0)
                    return [ct_section(ct, A, C, Az, Cz), [D[0], D[1]]]
            elif Cz > ct :
                if Dz < ct :    # A( 1) B( 1) C( 1) D(-1)
                    return [ct_section(ct, B, D, Bz, Dz), ct_section(ct, C, D, Cz, Dz)]
                else : # A( 1) B( 1) C( 1) D( 1) or # A( 1) B( 1) C( 1) D( 0)
                    return []
            else: 
                if Dz < ct :    # A( 1) B( 1) C( 0) D(-1)
                    return [ct_section(ct, B, D, Bz, Dz), [C[0], C[1]]]
                elif Dz > ct :  # A( 1) B( 1) C( 0) D( 1)
                    return []
                else:           # A( 1) B( 1) C( 0) D( 0)
                    return [[C[0], C[1]], [D[0], D[1]]]
        else: 
            if Cz < ct :
                # A( 1) B( 0) C(-1) D(-1)
                # A( 1) B( 0) C(-1) D( 1) and # A( 1) B( 0) C(-1) D( 0) impossible.
                return [ct_section(ct, A, C, Az, Cz), [B[0], B[1]]]
            elif Cz > ct :
                if Dz < ct :    # A( 1) B( 0) C( 1) D(-1)
                    return [ct_section(ct, C, D, Cz, Dz), [B[0], B[1]]]
                elif Dz > ct :  # A( 1) B( 0) C( 1) D( 1)
                    return []
                else:           # A( 1) B( 0) C( 1) D( 0)
                    return [[D[0], D[1]], [B[0], B[1]]]
            else:    # A( 1) B( 0) C( 0) D(-1)
                     # A( 1) B( 0) C( 0) D( 1) and # A( 1) B( 0) C( 0) D( 0) impossible
                return [[C[0], C[1]], [B[0], B[1]]]
    else: 
        if Bz < ct :
            if Cz < ct :
                # A( 0) B(-1) C(-1) D(-1)
                # A( 0) B(-1) C(-1) D( 1)
                # A( 0) B(-1) C(-1) D( 0)
                return []
            elif Cz > ct :
                if Dz < ct :    # A( 0) B(-1) C( 1) D(-1)
                    return [[A[0], A[1]], ct_section(ct, C, D, Cz, Dz)]
                elif Dz > ct :  # A( 0) B(-1) C( 1) D( 1)
                    return [[A[0], A[1]], ct_section(ct, B, D, Bz, Dz)]
                else:           # A( 0) B(-1) C( 1) D( 0)
                    return [[A[0], A[1]], [D[0], D[1]]]
            else: 
                # A( 0) B(-1) C( 0) D(-1)
                # A( 0) B(-1) C( 0) D( 1) impossible
                # A( 0) B(-1) C( 0) D( 1) impossible
                return [[A[0], A[1]], [C[0], C[1]]]
        elif Bz > ct :
            if Cz < ct :
                if Dz < ct :    # A( 0) B( 1) C(-1) D(-1)
                    return [[A[0], A[1]], ct_section(ct, B, D, Bz, Dz)]
                elif Dz > ct :  # A( 0) B( 1) C(-1) D( 1)
                    return [[A[0], A[1]], ct_section(ct, C, D, Cz, Dz)]
                else:           # A( 0) B( 1) C(-1) D( 0)
                    return [[A[0], A[1]], [D[0], D[1]]]
            elif Cz > ct :
                # A( 0) B( 1) C( 1) D(-1)
                # A( 0) B( 1) C( 1) D( 1)
                # A( 0) B( 1) C( 1) D( 0)
                return []
            else:
                # A( 0) B( 1) C( 0) D( 1)
                # A( 0) B( 1) C( 0) D(-1) impossible
                # A( 0) B( 1) C( 0) D( 0) impossible
                return [[A[0], A[1]], [C[0], C[1]]]
        else: 
            if Cz is not ct :
                # A( 0) B( 0) C(-1) D(-1)
                # A( 0) B( 0) C(-1) D( 1) impossible
                # A( 0) B( 0) C(-1) D( 0) impossible
                # A( 0) B( 0) C( 1) D( 1)
                # A( 0) B( 0) C( 1) D(-1) impossible
                # A( 0) B( 0) C( 1) D( 0) impossible
                return [[A[0], A[1]], [B[0], B[1]]]
            else:
                # A( 0) B( 0) C( 0) D( 0)
                # A( 0) B( 0) C( 0) D(-1) impossible
                # A( 0) B( 0) C( 0) D( 1) impossible
                return [[A[0], A[1]], [B[0], B[1]],
                        [B[0], B[1]], [D[0], D[1]],
                        [D[0], D[1]], [C[0], C[1]],
                        [C[0], C[1]], [A[0], A[1]]]
    
def ct_slice_of_quads(segments, ct) :
    """
    segments = [[[x1, y1, ct1], [x2, y2, ct2]],
                [[x3, y3, ct3], [x4, y4, ct4]],
             ...]
    returns : some lines [[x1, y1], [x2, y2], ....] since cti = ct for all i.
    """    
    if len(segments) < 2:
        return None
    res = []
    for (A, B), (C, D) in zip(segments[:-1], segments[1:]):
        res += slice_lines_of_quad(ct, A, B, C, D)
    if len(res) > 0 :
        return np.array(res)
    else:
        return None
    
