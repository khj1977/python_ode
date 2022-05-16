from numpy import linalg as la
import numpy as np

a21 = -6.0
a22 = -5.0
k1 = -1.0 * (10.0 + 20.0) + 6.0
k2 = -1.0 * (10.0 * 20.0) + 5.0
a = np.array([[0., 1.], [a21 + k1, a22 + k2]])
w, v = la.eig(a)
print(w)

w, v = la.eig(np.array([[0.0, 1.0], [-6.0, -5.0]]))
print(w)

w, v = la.eig(np.array([[0.0, 1.0], [-60.0, -50.0]]))
print(w)