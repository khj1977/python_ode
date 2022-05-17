import math
import matplotlib.pyplot as plt

data = []
ts = []

omega = 1.0

for t in range(0, 100):
    y = math.sin(omega * t)
    ts.append(t)
    data.append(y)

plt.ylim(-2, 2)
plt.xlim(0, 100)
plt.plot(ts, data, label="actual system")
plt.legend()
plt.show()