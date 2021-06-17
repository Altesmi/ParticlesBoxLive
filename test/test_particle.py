import pytest
from src.particle import Particle


@pytest.fixture(scope="function")
def test_particle():
    return Particle(x=0.1, y=0.8, velx=0.0, vely=0.1, radius=0.05)


@pytest.fixture(scope="function")
def another_particle():

    return Particle(x=0.5, y=0.2, velx=0.1, vely=0.0, radius=0.1)


@pytest.fixture(scope="function")
def particle_outside_box():
    return Particle(x=2.0, y=2.0, velx=0.0, vely=0.0, radius=0.1)


def test_collidesParticle(test_particle, another_particle):

    assert not test_particle.collidesParticle(another_particle)


def test_checkAndHandleWallCollision(particle_outside_box):
    particle_outside_box.checkAndHandleWallCollisions()
    assert particle_outside_box.x == 0.9
    assert particle_outside_box.y == 0.9


def test_run_wall_collision(test_particle):
    test_particle.run(dt=1)
    assert test_particle.y == 0.9
