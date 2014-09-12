from django.shortcuts import render
from base.models import Group
from django.views.generic import ListView

# Create your views here.


class GroupList(ListView):
    """
    Out group list.
    """
    model = Group
    template_name = "base/group_list.html"