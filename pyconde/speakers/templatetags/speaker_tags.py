from django.template import Library


register = Library()


@register.inclusion_tag('speakers/speaker_box.html', takes_context=True)
def speaker_box(context, speaker):
    return {
        'name': unicode(speaker),
        'avatar': speaker.user.avatar,
        'user': speaker.user,
        'STATIC_URL': context['STATIC_URL']
    }
