from django.shortcuts import get_object_or_404, get_list_or_404
from base.models import Group, Student
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse
from base.forms import GroupForm

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
        context['title'] = 'Stident list group {}'.format(
            self.kwargs['group_id'], )
        return context

    def get_queryset(self):
        return get_list_or_404(Student, group__pk=self.kwargs['group_id'])


class GroupAdd(CreateView):
    """
    add group
    """
    model = Group
    fields = ['name', ]
    template_name = "base/group_add.html"

    def get_context_data(self, **kwargs):
        context = super(GroupAdd, self).get_context_data(**kwargs)
        context['title'] = 'Group add'
        return context

    def get_success_url(self):
        return reverse('group_list')


class GroupEdit(UpdateView):
    """
    update group
    """
    fields = ['name', 'headman']
    template_name = "base/group_edit.html"
    model = Group
    form_class = GroupForm

    def get_context_data(self, **kwargs):
        context = super(GroupEdit, self).get_context_data(**kwargs)
        context['title'] = 'Group edit {}'.format(self.object, )
        return context

    def get_success_url(self):
        return reverse('group_list')

    def get_object(self, queryset=None):
        return get_object_or_404(Group, pk=self.kwargs['group_id'])


class GroupDelete(DeleteView):
    """
    Delete group
    """
    template_name = "base/group_delete.html"

    def get_success_url(self):
        return reverse('group_list')

    def get_object(self, queryset=None):
        return get_object_or_404(Group, pk=self.kwargs['group_id'])


class StudentAdd(CreateView):
    """
    student add
    """
    model = Student
    template_name = "base/student_add.html"

    def get_context_data(self, **kwargs):
        context = super(StudentAdd, self).get_context_data(**kwargs)
        context['title'] = 'Student add'
        return context

    def get_success_url(self):
        return reverse('group_list')


class StudentEdit(UpdateView):
    """
    edint student
    """
    template_name = "base/student_edit.html"
    model = Student
    fields = ['fio', ]

    def get_context_data(self, **kwargs):
        context = super(StudentEdit, self).get_context_data()
        context['title'] = 'Student edit {}'.format(
            self.object, )
        return context

    def get_success_url(self):
        return reverse("group_list")

    def get_object(self, queryset=None):
        #return get_object_or_404(Student, pk=self.kwargs['student_id'])
        return Student.objects.get(pk=self.kwargs['student_id'])