import numpy as np
from src.simulation import Simulation
from plotting.animation import createAnimation

numParticles = 20
radii = np.random.uniform(size=(numParticles, ))*0.02+0.01  # random number between [0.01, 0.03]

outputfile = 'results_10s.csv'

sim = Simulation(numParticles, radii)

sim.run(10, 0.01)

sim.writeOut(outputfile)

createAnimation(outputfile, 'results10s.gif', 200)
