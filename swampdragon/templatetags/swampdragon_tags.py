from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag()
def swampdragon_settings():
    root_url = getattr(settings, 'DRAGON_URL') or 'http://localhost:9999/'
    if not root_url.endswith('/'):
        root_url += '/'
    return mark_safe('<script type="text/javascript" src="{}settings.js"></script>'.format(root_url))
