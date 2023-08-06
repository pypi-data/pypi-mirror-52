from process.conf import get_conf
from .generic_views import (
    ProcessGenericCreateView,
    ProcessGenericListView,
    ProcessGenericUpdateView,
    ProcessGenericDeleteView
)
from ..forms import ParentRelationForm
from process.templatetags.parent_tasks import parent_badge_html


from process.models import Task


class TaskListView(ProcessGenericListView):
    model = Task
    title = 'Tasks'
    filters = get_conf('views__task__list__url_allow_filters')
    permissions = get_conf('views__task__list__permissions')


class TaskDeleteView(ProcessGenericDeleteView):
    model = Task
    success_url = get_conf('views__task__delete__success_url')
    success_message = get_conf('views__task__delete__success_message')
    permissions = get_conf('views__task__delete__permissions')


class TaskCreateView(ProcessGenericCreateView):
    model = Task
    success_url = get_conf('views__task__create__success_url')
    success_message = get_conf('views__task__create__success_message')
    permissions = get_conf('views__task__create__permissions')


class TaskUpdateView(ProcessGenericUpdateView):
    model = Task
    template_name = get_conf('views__templates__task_edit')
    success_url = get_conf('views__task__update__success_url')
    success_message = get_conf('views__task__update__success_message')
    permissions = get_conf('views__task__update__permissions')
    fields = [
        'name',
        'description',
        'is_active',
        'level',
        'offset',
        'interpreter',
        'arguments',
        'code',
    ]

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()

        context['parent_badge_html'] = parent_badge_html

        # we get the tasks which can be parent
        context['parent_options'] = self.object.process.tasks.all().\
            exclude(id=self.object.id). \
            exclude(id__in=self.object.parents.all().values('parent')). \
            values('id', 'name')

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        print(f'got request {request.POST}')

