from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag()
def swampdragon_settings():
    root_url = getattr(settings, 'DRAGON_URL') or 'http://localhost:9999/'
    if not root_url.endswith('/'):
        root_url += '/'
    return '<script type="text/javascript" src="{}settings.js"></script>'.format(root_url)
