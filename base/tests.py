from django.test import TestCase
from base.models import Group

# Create your tests here.


class MyTestCase(TestCase):
    """
    test login and add group and student
    """
    def setUp(self):
        pass

    def test_login(self):
        """

        :return: test login
        """
        self.client.post('/login/', {'username': 'admin', 'password': 'admin'})

    def test_add_group_student(self):
        """

        :return: test add group and student
        """
        group_name = 'group 1'
        self.client.post('/groups/add/', {'name': 'group 1'})
        self.assertTrue(Group.objects.all().exists())