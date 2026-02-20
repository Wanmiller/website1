from django import template

register = template.Library()


@register.filter
def rating_badge(value):
    try:
        rating = float(value)
    except (TypeError, ValueError):
        return "N/A"
    if rating >= 4:
        return f"Excellent ({rating:.1f})"
    if rating >= 3:
        return f"Good ({rating:.1f})"
    return f"Needs work ({rating:.1f})"
