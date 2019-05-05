from helpers import normalize
import numpy as np
import math


class Plane:
    def __init__(self, point, normal, material):
        self.point = point
        self.normal = normalize(normal)
        self.material = material

    def intersection_parameter(self, ray):
        op = ray.origin - self.point
        a = np.dot(op, self.normal)
        b = np.dot(ray.direction, self.normal)
        if b:
            return -a / b
        else:
            return None

    def normal_at(self, p):
        return self.normal


class Sphere:
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def intersection_parameter(self, ray):
        co = self.center - ray.origin
        v = np.dot(co, ray.direction)
        discriminant = v * v - np.dot(co, co) + self.radius * self.radius
        if discriminant < 0:
            return None
        else:
            return v - math.sqrt(discriminant)

    def normal_at(self, p):
        return normalize(p - self.center)


class Triangle:
    def __init__(self, a, b, c, material):
        self.a = a
        self.b = b
        self.c = c
        self.u = self.b - self.a
        self.v = self.c - self.a
        self.material = material

    def intersection_parameter(self, ray):
        w = ray.origin - self.a
        dv = np.cross(ray.direction, self.v)
        dvu = np.dot(dv, self.u)
        if dvu == 0:
            return None
        wu = np.cross(w, self.u)
        r = np.dot(dv, w) / dvu
        s = np.dot(wu, ray.direction) / dvu
        if 0 <= r <= 1 and 0 <= s <= 1 and r+s <= 1:
            return np.dot(wu, self.v) / dvu
        else:
            return None

    def normal_at(self, p):
        return normalize(np.cross(self.u, self.v))
