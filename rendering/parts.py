import math
import numpy as np
from helpers import normalize
from objects.material import Color


class Camera:

    def __init__(self, e, u, c, fov, image_width, image_height):
        self.e = e
        self.u = u
        self.c = c
        self.fov = fov
        self.image_width = image_width
        self.image_height = image_height

        self.f = normalize(self.c - self.e)
        self.s = normalize(np.cross(self.f, u))
        self.u = np.cross(self.s, self.f) * -1

        self.alpha = fov / 2
        self.height = 2 * math.tan(self.alpha * math.pi / 180.0)
        self.width = self.height * (image_width/float(image_height))

        self.pixelWidth = self.width / image_width
        self.pixelHeight = self.height / image_height

    def calc_ray(self, x, y):
        x_comp = self.s * (x * self.pixelWidth - self.width / 2.)
        y_comp = self.u * (y * self.pixelHeight - self.height / 2.)
        return Ray(self.e, self.f + x_comp + y_comp)


class Light:
    def __init__(self, position):
        self.position = position
        self.color = Color((255, 255, 255))


class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = normalize(direction)

    def point_at_parameter(self, t):
        return self.origin + self.direction * t
