from django.shortcuts import get_object_or_404, get_list_or_404
from base.models import Group, Student
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse
from base.forms import GroupForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

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


class GroupAdd(CreateView):
    """
    add group
    """
    model = Group
    fields = ['name', ]
    template_name = "base/group_add.html"

    @method_decorator(login_required(login_url='/login'))
    def dispatch(self, request, *args, **kwargs):
        return super(GroupAdd, self).dispatch(request, *args, **kwargs)

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
    pk_url_kwarg = 'group_id'

    def get_context_data(self, **kwargs):
        context = super(GroupEdit, self).get_context_data(**kwargs)
        context['title'] = 'Group edit {}'.format(self.object, )
        return context

    def get_success_url(self):
        return reverse('group_list')


class GroupDelete(DeleteView):
    """
    Delete group
    """
    template_name = "base/group_delete.html"
    model = Group
    pk_url_kwarg = 'group_id'

    def get_success_url(self):
        return reverse('group_list')


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
        context['group_id'] = self.kwargs['group_id']
        return context

    def get_queryset(self):
        return get_list_or_404(Student, group__pk=self.kwargs['group_id'])

    #@method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super(StudentList, self).dispatch(request, *args, **kwargs)


class StudentAdd(CreateView):
    """
    student add
    """
    model = Student
    template_name = "base/student_add.html"

    def get_context_data(self, **kwargs):
        context = super(StudentAdd, self).get_context_data(**kwargs)
        context['title'] = 'Student add'
        context['group_id'] = self.request.GET['group_id']
        return context

    def get_success_url(self):
        return reverse("student_list", kwargs={
            'group_id': self.object.group.pk})


class StudentEdit(UpdateView):
    """
    edit student
    """
    model = Student
    template_name = "base/student_edit.html"
    pk_url_kwarg = 'student_id'

    def get_context_data(self, **kwargs):
        context = super(StudentEdit, self).get_context_data(**kwargs)
        context['title'] = 'Student edit {}'.format(
            self.object, )
        context['group_id'] = self.object.group.pk
        return context

    def get_success_url(self):
        return reverse("student_list", kwargs={
            'group_id': self.object.group.pk})


class StudentDelete(DeleteView):
    """
    delete student
    """
    model = Student
    template_name = "base/student_delete.html"
    pk_url_kwarg = 'student_id'

    def get_context_data(self, **kwargs):
        context = super(StudentDelete, self).get_context_data(**kwargs)
        context['title'] = 'Delete student {}'.format(self.object)
        context['group_id'] = self.object.group.pk
        return context

    def get_success_url(self):
        return reverse("student_list", kwargs={
            'group_id': self.object.group.pk})
        #return reverse('group_list')