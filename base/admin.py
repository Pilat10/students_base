from django.contrib import admin
from base.models import Student, Group
from base.signal_models import LogEntry
from base.forms import GroupForm

# Register your models here.


class StudentInline(admin.TabularInline):
    model = Student


class GroupAdmin(admin.ModelAdmin):
    form = GroupForm
    inlines = [StudentInline, ]
admin.site.register(Group, GroupAdmin)
admin.site.register(Student)
admin.site.register(LogEntry)
