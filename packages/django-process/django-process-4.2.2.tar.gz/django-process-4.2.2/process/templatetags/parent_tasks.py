from django import template
from django.utils.safestring import mark_safe

register = template.Library()

parent_badge_html = """
<div class="btn btn-primary d-flex justify-content-between mb-1" style="cursor: default;">
    <input type="hidden" name="parents" value="{id}">
    <span>{name}</span>
    <span class="badge badge-light" style="cursor: pointer;" onclick="removeParentTask(this);">X</span>
</div>
"""


@register.filter(name='as_badges', is_safe=True)
def as_badges(parents):
    response = ''
    for parent in parents:
        response += parent_badge_html.strip().format(id=parent.id, name=parent.parent.name)
    return mark_safe(response)
