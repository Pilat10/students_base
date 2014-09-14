from django.shortcuts import render
from base.models import Group, Student
from django.views.generic import ListView, CreateView
from django.core.urlresolvers import reverse

# Create your views here.


class GroupList(ListView):
    """
    Out groups list.
    """
    model = Group
    template_name = "base/group_list.html"
    context_object_name = "group_list"

    def get_context_data(self, **kwargs):
        context = super(GroupList, self).get_context_data(**kwargs)
        context['title'] = "Group list"
        return context


class StudentList(ListView):
    """
    Out students list
    """
    template_name = "base/student_list.html"
    context_object_name = "student_list"

    def get_context_data(self, **kwargs):
        context = super(StudentList, self).get_context_data(**kwargs)
        context['title'] = 'Stident list group %s' % self.kwargs['group_id']
        return context

    def get_queryset(self):
        return Student.objects.filter(group__pk=self.kwargs['group_id'])


class GroupAdd(CreateView):
    """
    add group
    """
    model = Group
    fields = ['name', 'headman']
    template_name = "base/group_add.html"

    def get_context_data(self, **kwargs):
        context = super(GroupAdd, self).get_context_data(**kwargs)
        context['title'] = 'Group add'
        return context

    def get_success_url(self):
        return reverse('group_list')
