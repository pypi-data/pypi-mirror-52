from django import forms
from .models import Task, TaskDependence
from django.utils.translation import gettext_lazy as _


class ParentRelationForm(forms.ModelForm):
    id_relation = forms.CharField(
        widget=forms.HiddenInput(attrs={'name': 'id_relation[]', 'id': 'id_relation'})
    )
    parent = forms.ModelMultipleChoiceField(queryset=None)

    def __init__(self, process, *args, **kwargs):
        super().__init__(args, kwargs)
        self.fields['parent'].queryset = Task.objects.filter(process__id=process)

    class Meta:
        model = TaskDependence
        fields = ['id_relation', 'parent']
