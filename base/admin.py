from django.contrib import admin
from base.models import Student
from base.models import Group
from base.forms import GroupForm

# Register your models here.


class StudentInline(admin.TabularInline):
    model = Student


class GroupAdmin(admin.ModelAdmin):
    form = GroupForm
    inlines = [StudentInline, ]
admin.site.register(Group, GroupAdmin)
admin.site.register(Student)

