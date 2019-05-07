import math
import numpy as np
import settings
from threading import Thread
from PIL import Image
from objects.shape import Sphere, Triangle, Plane
from objects.material import Material, Color, CheckerboardMaterial
from rendering.parts import Camera, Light, Ray

# Settings
BACKGROUND_COLOR = Color((0, 0, 0))

MAX_LEVEL = settings.MAX_LEVEL

light = Light(np.array([20, 20, -5]))

e = np.array([0, 1.8, 10])
u = np.array([0, 1, 0])
c = np.array([0, 3, 0])
fov = 45

camera = Camera(e, u, c, fov, settings.IMAGE_HEIGHT, settings.IMAGE_WIDTH)

materials = {
    'red': Material(Color((255, 0, 0))),
    'green': Material(Color((0, 255, 0))),
    'blue': Material(Color((0, 0, 255))),
    'yellow': Material(Color((255, 255, 0)), 0),
    'checker_board': CheckerboardMaterial(Color((255, 255, 255))),
    'grey': Material(Color((10, 10, 10)), 0)
}

object_list = [
    Sphere(np.array([2.5, 2, -10]), 1.5, materials['red']),
    Sphere(np.array([-2.5, 2, -10]), 1.5, materials['green']),
    Sphere(np.array([0.0, 6, -10]), 1.5, materials['blue']),
    Triangle(np.array([2.5, 2, -10]), np.array([-2.5, 2, -10]), np.array([0, 6, -10]), materials['yellow']),
    Plane(np.array([0, 0, 0]), np.array([0, -1, 0]), materials['checker_board'])
]


def render(image, i):

    int_half_width = int(settings.IMAGE_WIDTH/2)
    int_half_height = int(settings.IMAGE_HEIGHT/2)

    if i > 1:
        y_multiplier = 1
    else:
        y_multiplier = 0

    for x in range(int_half_width):
        for y in range(int_half_height):
            ray = camera.calc_ray(x + i % 2 * int_half_width, y + y_multiplier * int_half_height)
            color = trace_ray(0, ray)

            image.putpixel((x + i % 2 * int_half_width, y + y_multiplier * int_half_height), color.get_color())


def main():
    image = Image.new('RGB', (settings.IMAGE_WIDTH, settings.IMAGE_HEIGHT))

    for i in range(4):
        t = Thread(target=render(image, i))
        t.start()

    image.show()
    image.save('scene.png', 'PNG')


def trace_ray(level, ray):
    if level < MAX_LEVEL:
        hit_point_data = intersect(ray)
        if hit_point_data:
            color = shade(level, hit_point_data, ray)
            target, point = hit_point_data

            light_ray = Ray(point, light.position - point)
            hit_point_data_shadow = intersect(light_ray)

            if hit_point_data_shadow and hit_point_data_shadow[0] is not target:
                color = color * 0.6
            return color

    return BACKGROUND_COLOR


def intersect(ray):
    max_dist = math.inf
    target_hit = None
    point_at_parameter = None
    for obj in object_list:
        hit_dist = obj.intersection_parameter(ray)
        if hit_dist:
            if 0 <= hit_dist < max_dist:
                max_dist = hit_dist
                target_hit = obj
                point_at_parameter = ray.point_at_parameter(hit_dist - 0.1)
    if target_hit is not None:
        return target_hit, point_at_parameter
    else:
        return None


def shade(level, hit_point_data, ray):
    target, point = hit_point_data
    direct_color = compute_direct_light(hit_point_data, ray)

    if settings.REFLECTION and target.material.shine > 0:
        reflected_ray = compute_reflected_ray(hit_point_data, ray)
        reflected_color = trace_ray(level + 1, reflected_ray)

        return direct_color + reflected_color * 0.4

    else:
        return direct_color


def compute_direct_light(hit_point_data, ray):
    target, point = hit_point_data
    light_ray = Ray(point, light.position - point)
    normal = target.normal_at(point)
    return target.material.calc_color(light, light_ray.direction, normal, ray, point)


def compute_reflected_ray(hit_point_data, ray):
    target, point = hit_point_data
    normal = target.normal_at(point)
    direction = ray.direction - normal * (2 * np.dot(ray.direction, normal))
    return Ray(point, direction)


if __name__ == '__main__':
    main()
