from django.forms import ModelForm, CharField
from base.models import Group


class GroupForm(ModelForm):
    """
    Group form chenge headman filds output
    """

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        self.fields['headman'].queryset = self.instance.student_set.all()
        #self.fields['dsss'] = CharField()
        #self.fields['dsss'].initial = self.instance.pk

    class Meta:
        model = Group