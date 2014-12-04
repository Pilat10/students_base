from django.forms import ModelForm
from base.models import Group


class GroupForm(ModelForm):
    """
    Group form chenge headman filds output
    """

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        self.fields['headman'].queryset = self.instance.student_set.all()

    class Meta:
        model = Group
        fields = "__all__"