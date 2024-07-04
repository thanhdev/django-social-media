from django import template
import re
from django.utils.html import escape
from django.utils.safestring import mark_safe

from home.utils import get_youtube_thumbnail

register = template.Library()
url_pattern = re.compile(
    r"(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|%[0-9a-fA-F][0-9a-fA-F])+)"  # noqa
)


@register.filter
def urlize(value):
    # Escape HTML characters
    value = escape(value)

    # Replace other URLs with clickable links
    value = url_pattern.sub(
        r'<a class="text-blue-500" href="\1"' r' target="_blank">\1</a>', value
    )

    # Add YouTube thumbnail if the URL is a YouTube video
    if thumbnail := get_youtube_thumbnail(value):
        value += f'<br><img src="{thumbnail}" style="max-width: 100%;">'

    return mark_safe(value)  # Mark the string as safe for HTML output
