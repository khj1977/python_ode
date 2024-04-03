# Introduction

This code is for numerical experiment or simulation of k-disturbance observer shown at my [M.Phil thesis](https://www.khj1977.net/mphil_thesis_additional/). For core of solver, euler method is used. Although the author knows existence of Runge-Kutta, it is thought that there are no reason to deploy Runge-Kutta and euler method is natural as mathematics of differential equation.

Since disturbance observer require some number of ODE solvers, ODE solver is enclosed on the class. Unlike general ODE solvers, there are several classes which corporate with each other and much number of object composition is used.

That's fine to just use this solver if one is non engineering student or even high school student. However, if one is engineering or science student and if one would go to post graduate school, it is better to modify this code for more general situation;i.e. high order systems or even multi-input systems.

With M1 Apple, this simulator is fast enough but if one want to deploy disturbance observer for robotics or even smart material systems, etc, it is better to implement by C++ or C with function pointer.

Robotics? Yes, this algorithm of robust control could be used to robotics as well. Or even, for active suspension of vehicle, it could be used.

# How to run?

At command line of mac or linux desktop evironment, execute the following command:

python batch-ode.py 

Several settings of ODE and init value or disturbance can be found on some files of python. More general way setting would be remain to further work of university student user.