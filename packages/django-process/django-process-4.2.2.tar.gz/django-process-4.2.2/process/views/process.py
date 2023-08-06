from process.conf import get_conf
from .generic_views import (
    ProcessGenericCreateView,
    ProcessGenericListView,
    ProcessGenericUpdateView,
    ProcessGenericDeleteView
)


from process.models import Process


class ProcessCreateView(ProcessGenericCreateView):
    model = Process
    success_url = get_conf('views__process__create__success_url')
    success_message = get_conf('views__process__create__success_message')
    permissions = get_conf('views__process__create__permissions')


class ProcessListView(ProcessGenericListView):
    model = Process
    title = 'Processes'
    filters = get_conf('views__process__list__url_allow_filters')
    permissions = get_conf('views__process__list__permissions')


class ProcessUpdateView(ProcessGenericUpdateView):
    model = Process
    success_url = get_conf('views__process__update__success_url')
    success_message = get_conf('views__process__update__success_message')
    permissions = get_conf('views__process__update__permissions')


class ProcessDeleteView(ProcessGenericDeleteView):
    model = Process
    success_url = get_conf('views__process__delete__success_url')
    success_message = get_conf('views__process__delete__success_message')
    permissions = get_conf('views__process__delete__permissions')
