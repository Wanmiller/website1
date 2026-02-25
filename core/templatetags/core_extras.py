from django import template
from django.utils.translation import gettext as _

register = template.Library()


@register.filter
def rating_badge(value):
    try:
        rating = float(value)
    except (TypeError, ValueError):
        return _("N/A")
    if rating >= 4:
        return _("%(level)s (%(rating).1f)") % {"level": _("Excellent"), "rating": rating}
    if rating >= 3:
        return _("%(level)s (%(rating).1f)") % {"level": _("Good"), "rating": rating}
    return _("%(level)s (%(rating).1f)") % {"level": _("Needs work"), "rating": rating}
