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

        amb_color = self.base_color_at_p(intersection) * self.ambient

        dif_color = light.color * self.diffuse * np.dot(light_direction, normal)

        if not settings.REFLECTION:
            return amb_color + dif_color
        else:
            lr = (light_direction - normal * (2 * abs(np.dot(light_direction, normal))))
            spec_color = light.color * self.specular * (np.dot(lr, -ray.direction)) ** self.shine

            return amb_color + dif_color + spec_color


class CheckerboardMaterial(Material):
    def __init__(self, color):
        super().__init__(color, 0)
        self.ambient = 1
        self.diffuse = 0.6
        self.specular = 0.2
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
