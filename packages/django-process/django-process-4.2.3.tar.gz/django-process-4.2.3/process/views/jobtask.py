from process.conf import get_conf
from .generic_views import (
    ProcessGenericListView,
    ProcessGenericDeleteView
)


from process.models import JobTask


class JobTaskListView(ProcessGenericListView):
    model = JobTask
    title = 'JobTasks'
    filters = get_conf('views__jobtask__list__url_allow_filters')
    permissions = get_conf('views__jobtask__list__permissions')


class JobTaskDeleteView(ProcessGenericDeleteView):
    model = JobTask
    success_url = get_conf('views__jobtask__delete__success_url')
    success_message = get_conf('views__jobtask__delete__success_message')
    permissions = get_conf('views__jobtask__delete__permissions')
