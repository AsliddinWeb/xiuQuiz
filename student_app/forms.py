from django import forms
from .models import Group, Student

class StudentSelectionForm(forms.Form):
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        label="Guruh",
        widget=forms.Select(attrs={'class': 'form-control', 'onchange': 'filterStudents(this)'}),
    )
    student = forms.ModelChoiceField(
        queryset=Student.objects.none(),
        label="Talaba",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    def __init__(self, *args, **kwargs):
        group_id = kwargs.pop('group_id', None)
        super().__init__(*args, **kwargs)
        if group_id:
            self.fields['student'].queryset = Student.objects.filter(group_id=group_id)
