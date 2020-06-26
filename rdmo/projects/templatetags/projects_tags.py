from django import template
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()


@register.simple_tag()
def get_question_for_attribute(attribute, questions):
    try:
        return questions.get(attribute=attribute).text
    except ObjectDoesNotExist:
        return ''
