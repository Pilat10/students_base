from django.core.management.base import BaseCommand
from base.models import Group


class Command(BaseCommand):
    """

    """

    def handle(self, *args, **options):
        for group in Group.objects.all():
            self.stdout.write(
                'group name {}, headman {}'.format(group.name, group.headman))
            for stud in group.student_set.all():
                self.stdout.write('   {}'.format(stud.fio))
