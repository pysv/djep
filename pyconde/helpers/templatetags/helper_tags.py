from urlparse import urlparse

from django.template import Library
from django.utils.html import escape
from django.utils.safestring import mark_safe


register = Library()


def shy(value, max_length=None):
    """
    Inserts &shy; elements in over-long strings.
    """
    if not max_length:
        return value
    result = []
    for word in value.split():
        if len(word) > max_length:
            # Split the word into chunks not larger than max_length
            nw = [word[i:i+max_length] for i in range(0, len(word), max_length)]
            result.append(u"&shy;".join(nw))
        else:
            result.append(word)
    return u" ".join(result)


@register.filter
def safe_and_shy(value, max_length=None):
    return mark_safe(shy(escape(value), max_length))


@register.filter
def domain(url):
    components = urlparse(url)
    netloc = components[1]
    if not netloc:
        return url
    return netloc
