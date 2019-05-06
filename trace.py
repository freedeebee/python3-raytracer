import math
import numpy as np
from PIL import Image
from objects.shape import Sphere, Triangle, Plane
from objects.material import Material, Color, CheckerboardMaterial
from rendering.parts import Camera, Light, Ray

# Settings
BACKGROUND_COLOR = Color((0, 0, 0))

IMAGE_WIDTH = IMAGE_HEIGHT = 400
MAX_LEVEL = 1

light = Light(np.array([30, 30, 10]), Color((255, 255, 255)))

e = np.array([0, 1.8, 10])
u = np.array([0.0, 1.0, 0])
c = np.array([0, 3, 0])
fov = 45

camera = Camera(e, u, c, fov, IMAGE_HEIGHT, IMAGE_WIDTH)

materials = {
    'red': Material(Color((255, 0, 0))),
    'green': Material(Color((0, 255, 0))),
    'blue': Material(Color((0, 0, 255))),
    'yellow': Material(Color((255, 255, 0)), 0),
    'checker_board': CheckerboardMaterial(Color((0, 180, 100))),
    'grey': Material(Color((40, 40, 40)))
}

object_list = [
    Sphere(np.array([2.5, 3, -10]), 2, materials['red']),
    Sphere(np.array([-2.5, 3, -10]), 2, materials['green']),
    Sphere(np.array([0.0, 7, -10]), 2, materials['blue']),
    Triangle(np.array([2.5, 3, -10]), np.array([-2.5, 3, -10]), np.array([0, 7, -10]), materials['yellow']),
    Plane(np.array([0, 0, 0]), np.array([0, 10, 0]), materials['checker_board'])
]


def main():
    image = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT))
    for x in range(IMAGE_WIDTH):
        for y in range(IMAGE_HEIGHT):
            ray = camera.calc_ray(x, y)
            color = trace_ray(0, ray)

            image.putpixel((x, y), color.get_color())
    image.show()
    image.save('scene.png', 'PNG')


def has_shadow(light_ray, obj):
    hit_point_data = intersect(light_ray)
    if hit_point_data and hit_point_data[1] is not obj:
        return True
    return False


def trace_ray(level, ray):
    if level >= MAX_LEVEL:
        return BACKGROUND_COLOR
    else:
        hit_point_data = intersect(ray)
    if hit_point_data:
        color = shade(level, hit_point_data, ray)
        intersection = hit_point_data[0]
        light_ray = Ray(intersection, light.position - intersection)
        if has_shadow(light_ray, hit_point_data[1]):
            color = color * 0.6
        return color

    return BACKGROUND_COLOR


def intersect(ray):
    max_dist = math.inf
    hitobj = None
    intersection = None
    counter = 0
    for obj in object_list:
        hitdist = obj.intersection_parameter(ray)
        if hitdist and 0 <= hitdist < max_dist:
            max_dist = hitdist
            hitobj = obj
            intersection = ray.point_at_parameter(hitdist - 0.0001)
            counter += 1
    if hitobj is not None:
        return intersection, hitobj, counter
    else:
        return None


def shade(level, hit_point_data, ray):
    direct_color = compute_direct_light(hit_point_data, ray)

    reflected_ray = compute_reflected_ray(hit_point_data, ray)
    reflected_color = trace_ray(level + 1, reflected_ray)

    return direct_color + reflected_color * 0.4


def compute_direct_light(hit_point_data, ray):
    intersection = hit_point_data[0]
    obj = hit_point_data[1]
    light_ray = Ray(intersection, light.position - intersection)
    normal = obj.normal_at(intersection)
    material = obj.material
    color = material.calc_color(light, light_ray.direction, normal, ray, intersection)
    return color


def compute_reflected_ray(hit_point_data, ray):
    intersection = hit_point_data[0]
    obj = hit_point_data[1]
    normal = obj.normal_at(intersection)
    dr = ray.direction - normal * (2*(np.dot(ray.direction, normal)))
    return Ray(intersection, dr)


if __name__ == '__main__':
    main()
