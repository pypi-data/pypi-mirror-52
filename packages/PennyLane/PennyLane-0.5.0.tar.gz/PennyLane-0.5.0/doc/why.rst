What PennyLane is designed for
==============================

PennyLane is designed to optimize gate parameters in quantum circuits via gradient descent -- whether they run on quantum hardware, or classical simulators. As a result, this has several implications that you should be aware of:

* You can easily swap different quantum simulators, or quantum simulators with quantum hardware, only changing one line of your code.

* PennyLane takes care to use analytic gradients wherever possible, according to the latest research :cite:`schuld2018evaluating`. It has been shown that the use of analytic gradients in gradient descent can lead to faster convergence of the optimization :cite:`harrow2019low`.

* You cannot access the wavefunction of the quantum state at any time. The only access to a quantum computation we have is through measurements (like in real life).

* While gradients of a hybrid computation are calculated using automatic differentiation, we do not know of a strategy to backpropagate errors through a quantum circuit.



+------------+-------------+------------------+---------------+
|            | macOS 10.6+ | manylinux x86_64 | Windows 64bit |
+============+=============+==================+===============+
| Python 3.5 |  ✅         |  ✅              |   ✅          |
+------------+-------------+------------------+---------------+
| Python 3.6 |  ✅         |  ✅              |   ✅          |
+------------+-------------+------------------+---------------+
| Python 3.7 |  ✅         |  ✅              |   ✅          |
+------------+-------------+------------------+---------------+

Benchmarking
============

To give you an idea of PennyLane scaling behavior, let us look at a simple example.

