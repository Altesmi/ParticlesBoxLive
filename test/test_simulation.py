import numpy as np
import pytest
from src.simulation import Simulation


@pytest.fixture(scope="function")
def test_simulation():
    numParticles = 2
    radii = np.repeat([0.05], repeats=numParticles)
    sim = Simulation(numParticles=numParticles, radii=radii)
    # Change the two particles so that they collide
    sim.particles[0].x = 0.1
    sim.particles[0].y = 0.1
    sim.particles[0].velx = 0.1
    sim.particles[0].vely = 0.0

    sim.particles[1].x = 0.19
    sim.particles[1].y = 0.1
    sim.particles[1].velx = -0.1
    sim.particles[1].vely = 0.0

    return sim


def test_checkAndhandleParticleCollision(test_simulation):
    test_simulation.checkAndHandleParticleCollisions()
    assert pytest.approx(test_simulation.particles[0].velx, rel=1e-10) == -0.1
