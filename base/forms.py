from django.forms import ModelForm
from base.models import Group, Student


class GroupForm(ModelForm):
    """
    Group form chenge headman filds output
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['headman'].queryset = self.instance.student_set.all()
        else:
            self.fields['headman'].queryset = Student.objects.none()

    class Meta:
        model = Group
        fields = "__all__"
