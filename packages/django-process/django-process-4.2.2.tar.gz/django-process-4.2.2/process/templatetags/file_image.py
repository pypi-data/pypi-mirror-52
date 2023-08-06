from django import template

from process.conf import get_conf

register = template.Library()


@register.filter(name='get_image', is_safe=True)
def get_image(extension):
    path = get_conf(f'views__templates__extension_images__{extension}')
    return path
