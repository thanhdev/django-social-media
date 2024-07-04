from django import template
import re
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def urlize(value):
    url_pattern = re.compile(
        r'(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)')
    value = escape(value)  # Escape HTML characters
    value = url_pattern.sub(r'<a href="\1" target="_blank">\1</a>', value)
    return mark_safe(value)  # Mark the string as safe for HTML output
