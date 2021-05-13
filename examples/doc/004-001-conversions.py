import relativipy as rel
import numpy as np

# Here we illustrate usefull computation involving the change of frame
# of reference, i.e. the use of the lorrentz transform.

# R1 is moving at speed S relatively to R0.

C = 1.                     # The speed of light
S = np.array([C/2, -C/10]) # The speed of R1 in R0

xyt_events_R0  = np.array([(1, 2, 3), (1, 2, 4), (4, 2, 1)])
xyCt_events_R0 = xyt_events_R0 * np.array([1, 1, C])

# L transorm xyCT events expressed in R0 into the same events but
# expressed as xyCT in R1
L = rel.lorentz.direct(S, C)

xyCt_events_R1 = rel.lorentz.transform(L, xyCt_events_R0)

# iL transorm xyCT events expressed in R1 into the same events but
# expressed as xyCT in R0
iL = rel.lorentz.inverse(S, C) # This is rel.lorentz.direct(-S, C)
print('This should be close to 0 : {}'.format(np.max(rel.lorentz.transform(iL, xyCt_events_R1) - xyCt_events_R0)))



