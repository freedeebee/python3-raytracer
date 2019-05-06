import numpy as np
import settings


class Material:
    def __init__(self, color, shine=settings.SHINE):
        self.color = color
        self.ambient = settings.AMBIENT
        self.diffuse = settings.DIFFUSE
        self.specular = settings.SPECULAR
        self.shine = shine

    def base_color_at_p(self, p):
        return self.color

    def calc_color(self, light, light_direction, normal, ray, intersection):
        scalar = np.dot(light_direction, normal)

        amb_color = self.base_color_at_p(intersection) * self.ambient

        dif_color = light.color * self.diffuse * scalar

        lr = (light_direction - normal * (2 * abs(scalar)))
        spec_color = light.color * self.specular * (np.dot(lr, ray.direction * -1)) ** self.shine

        return amb_color + dif_color


class CheckerboardMaterial(Material):
    def __init__(self, color):
        super(CheckerboardMaterial, self).__init__(color)
        self.baseColor = color
        self.otherColor = Color((0, 0, 0))
        self.checkSize = 1

    def base_color_at_p(self, p):
        v = np.array([p[0], p[1], p[2]])
        v * (1 / self.checkSize)
        if (int(abs(v[0]) + 0.5) + int(abs(v[1]) + 0.5) + int(abs(v[2]) + 0.5)) % 2:
            return self.otherColor
        return self.baseColor


class Color:
    def __init__(self, color):
        self.color = color

    def __mul__(self, other):
        return Color(tuple(map(lambda x: x * other, self.color)))

    def __add__(self, other):
        return Color(tuple(map(lambda x, y: x + y, self.color, other.color)))

    def get_color(self):
        return tuple(map(int, self.color))
