from numpy import linalg as la
import numpy as np

a21 = -6.0
a22 = -5.0
#a21 = -2.0
#a22 = -1.0
l1 = 10.0
l2 = 20.0
k2 = -1.0 * (l1 + l2) - a22
k1 = -1.0 * (l1 * l2) - a21
a = np.array([[0., 1.], [a21 + k1, a22 + k2]])
w, v = la.eig(a)
print(w)

w, v = la.eig(np.array([[0.0, 1.0], [a21, a22]]))
print(w)

#w, v = la.eig(np.array([[0.0, 1.0], [-6.0, -5.0]]))
#print(w)

#w, v = la.eig(np.array([[0.0, 1.0], [-60.0, -50.0]]))
#print(w)