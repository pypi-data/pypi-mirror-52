from process.conf import get_conf
from .generic_views import (
    ProcessGenericListView,
    ProcessGenericDeleteView
)


from process.models import Job


class JobListView(ProcessGenericListView):
    model = Job
    title = 'Jobs'
    filters = get_conf('views__job__list__url_allow_filters')
    permissions = get_conf('views__job__list__permissions')


class JobDeleteView(ProcessGenericDeleteView):
    model = Job
    success_url = get_conf('views__job__delete__success_url')
    success_message = get_conf('views__job__delete__success_message')
    permissions = get_conf('views__job__delete__permissions')
