from __future__ import annotations
import numpy as np


class Particle:
    """ Models real world particles as elastic circles

    Attributes:
            coordinates (np.ndarray): horizontal and vertical coordinates of the center of the circle (L)
            vel (np.ndarray): horizontal and vertical velocity of the center of the circle (L/T)
            r (float): radius of the circle (L)
    """

    def __init__(self, x: float, y: float, velx: float, vely: float, radius: float):
        """ Initializes particles

        Args:
            x (float): Horizontal coordinate
            y (float): Vertical coordinate
            velx (float): Vertical velocity
            vely (float): Horizontal velocity
            radius (float): Radius of the circle
        """
        self.coordinates = np.array((x, y))
        self.vel = np.array((velx, vely))
        self.r = radius

    @property
    def x(self):
        return self.coordinates[0]

    @x.setter
    def x(self, value: float):
        self.coordinates[0] = value

    @property
    def y(self):
        return self.coordinates[1]

    @y.setter
    def y(self, value: float):
        self.coordinates[1] = value

    @property
    def velx(self):
        return self.vel[0]

    @velx.setter
    def velx(self, value: float):
        self.vel[0] = value

    @property
    def vely(self):
        return self.vel[1]

    @vely.setter
    def vely(self, value: float):
        self.vel[1] = value

    def collidesParticle(self, p2: Particle) -> bool:
        """ Checks if the distance between self and p2 is less than the sum of their radii
        i.e. have the to particles collided

        Args:
            p2 (Particle): Another particle

        Returns:
            bool: True if this particle collides with p2, False otherwise
        """

        return np.sqrt(np.sum((self.coordinates - p2.coordinates)**2)) < self.r+p2.r

    def checkAndHandleWallCollisions(self) -> None:
        """ Changes particle position such that it is always inside a unit rectangle.
        """
        if self.x - self.r < 0:
            self.x = self.r
            self.velx = -self.velx
        if self.x + self.r > 1:
            self.x = 1-self.r
            self.velx = -self.velx
        if self.y - self.r < 0:
            self.y = self.r
            self.vely = -self.vely
        if self.y + self.r > 1:
            self.y = 1-self.r
            self.vely = -self.vely

    def run(self, dt: float) -> None:
        """Advances partice position from current time to time+dt assuming constant velocity

         Args:
             dt (float): time step
         """

        self.coordinates = self.coordinates + self.vel*dt
        self.checkAndHandleWallCollisions()
