from typing import Tuple
import numpy as np
import pandas as pd
from itertools import combinations
from src.particle import Particle


class Simulation:
    """Simulation class for particles in a box. Simulation domain is a unit rectangle.

     Attributes:
            particles (np.ndarray): collection of all the particles
            time (float): time in the simulation (s)
            results (pd.DataFrame): results dataframe where the particle positions and velocities are recorded
    """

    def __init__(self, numParticles: int, radii: np.ndarray):
        """Initializes simulation

        Args:
            numParticles (int): number of particles to be created
            radii (np.ndarray): Radius of each particle
        """
        self.particles: np.ndarray = np.array([], dtype=object)
        self.numParticles = numParticles
        self.time: float = 0.0
        self.results: pd.DataFrame = pd.DataFrame(columns=['time', 'nParticle', 'radius', 'x', 'y', 'velx', 'vely'])

        for i in range(numParticles):
            while True:
                x, y = np.random.uniform(size=(2,))*(1-2*radii[i])+radii[i]
                vr = 0.02*np.random.uniform()+0.001
                velphi = 2.0*np.pi*np.random.uniform()
                velx, vely = vr*np.cos(velphi), vr*np.sin(velphi)
                p = Particle(x, y, velx, vely, radii[i])
                collidesFlag = False
                for p2 in self.particles:
                    if p2.collidesParticle(p):
                        collidesFlag = True
                        break
                if collidesFlag:
                    continue
                else:
                    self.particles = np.append(self.particles, p)
                    break

    def handleParticleCollision(self, p1: Particle, p2: Particle) -> Tuple:
        """Changes velocity of particles that have collided

        Args:
            p1 (Particle): First particle
            p2 (Particle): Second particle

        Returns:
            Tuple: first element is p2 and second p2 whose velocities have been updated following collision

        References:
            htts://en.wikipedia.org/wiki/Elastic_collision
        """
        m1 = p1.r**2
        m2 = p2.r**2
        dSquared = np.linalg.norm(p1.coordinates-p2.coordinates)**2
        u1 = p1.vel - 2*m2 * np.dot(p1.vel - p2.vel, p1.coordinates-p2.coordinates) \
            * (p1.coordinates-p2.coordinates)/(m1+m2)/dSquared
        u2 = p2.vel - 2*m1 * np.dot(p2.vel - p1.vel, p2.coordinates - p1.coordinates)\
            * (p2.coordinates-p1.coordinates) / (m1+m2) / dSquared
        p1.vel = u1
        p2.vel = u2

        return (p1, p2)

    def checkAndHandleParticleCollisions(self) -> None:
        """Check and update velocities of every particle if they've collided
        """
        pairs = combinations(range(self.numParticles), 2)

        for i, j in pairs:
            if self.particles[i].collidesParticle(self.particles[j]):
                self.particles[i], self.particles[j] = self.handleParticleCollision(
                    self.particles[i], self.particles[j])

    def run(self, timeEnd: float, dt: float) -> None:
        """Advances simulation ti timeEnd with time step dt

        Args:
            timeEnd (float): Ending time of the simulation (T)
            dt (float): simulation time step (T)
        """

        while self.time <= timeEnd:
            for p in self.particles:
                p.run(dt)
            self.checkAndHandleParticleCollisions()
            self.time = self.time+dt
            self.updateResults(self.time)

    def updateResults(self, time: float) -> None:
        """Appends current position and velocity of particles to results dataframe

        Args:
            time (float): Current time in the simulation. Will be included in results dataframe
        """
        ind = self.results.shape[0]

        for i, p in enumerate(self.particles):
            self.results.loc[ind] = [time, i, p.r, p.x, p.y, p.velx, p.vely]
            ind = ind+1

    def writeOut(self, outputfile: str) -> None:
        """Saves the results to csv file. The filename is speciefied in outputfile when creating the simulation object.

        Args:
            outputfile (str): name of the output file

        """
        self.results.to_csv(outputfile)
