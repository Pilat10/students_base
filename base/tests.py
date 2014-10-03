from django.test import TestCase
from base.models import Group, Student
from django.contrib.auth.models import User

# Create your tests here.


class MyTestCase(TestCase):
    """
    test login and add group and student
    """
    def setUp(self):
        User.objects.create_user('admin','admin@admin.admin', 'admin')
        pass

    def test_add_group_student(self):
        """

        :return: test add group and student
        """
        login = self.client.login(username='admin', password='admin')
        self.assertTrue(login)
        group_name = 'group 1'
        self.client.post('/groups/add/', {'name': group_name})
        self.assertTrue(Group.objects.all().exists())
        group = Group.objects.get(name=group_name)
        self.client.post('/student/add/', {
            'fio': 'Anton',
            'birthday': '1991-04-01',
            'number_student_cart': '124364',
            'group': group.pk, })
        self.assertTrue(Student.objects.all().exists())
