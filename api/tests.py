from rest_framework.test import APITestCase
from rest_framework.status import *
from django.contrib.auth.models import User, Group as Group_auth, Permission
from serializers import DepartmentSerializer
from datetime import date
from base.models import Department, Group, Student
from django.core.urlresolvers import reverse

SUCCESS_STATUS = 'success'
FAIL_STATUS = 'fail'

class AuthenticationTastCase(APITestCase):
    """
    test api login, logout, authentication
    """
    def setUp(self):
        User.objects.create_user('admin', 'admin@admin.admin', 'admin')
        self.user = {
            "username": "admin",
            "password": "admin",
        }
        self.auth_url = reverse("api:auth")

    def test_login_fail(self):
        """
        test api login fail
        """
        user_fail = {
            "username": "fail_admin",
            "password": "admin",
        }
        login = self.client.post(self.auth_url, user_fail)
        self.assertEqual(login.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(login.data.get("status"), FAIL_STATUS)

    def test_login_success(self):
        """
        test api login success
        """
        login = self.client.post(self.auth_url, self.user)
        self.assertEqual(login.status_code, HTTP_200_OK)
        self.assertEqual(login.data.get("status"), SUCCESS_STATUS)

    def test_auth_success(self):
        """
        test api auth success
        """
        self.client.post(self.auth_url, self.user)
        auth = self.client.get(self.auth_url)
        self.assertEqual(auth.status_code, HTTP_200_OK)
        self.assertEqual(auth.data.get("status"), SUCCESS_STATUS)
        data = auth.data.get("data")
        self.assertEqual(data["user"], "admin")

    def test_auth_fail(self):
        """
        test api auth success
        """
        auth = self.client.get(self.auth_url)
        self.assertEqual(auth.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(auth.data.get("status"), FAIL_STATUS)
        data = auth.data.get("data")
        self.assertEqual(data["user"], "AnonymousUser")

    def test_logout(self):
        """
        test api logout
        """
        login = self.client.post(self.auth_url, self.user)
        self.assertEqual(login.status_code, HTTP_200_OK)
        self.assertEqual(login.data.get("status"), SUCCESS_STATUS)
        logout = self.client.delete(self.auth_url)
        self.assertEqual(logout.status_code, HTTP_200_OK)
        auth = self.client.get(self.auth_url)
        self.assertEqual(auth.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(auth.data.get("status"), FAIL_STATUS)
        data = auth.data.get("data")
        self.assertEqual(data["user"], "AnonymousUser")


class DepartmentTestCase(APITestCase):
    """
    test api department get, post, put, delete
    """
    fixtures = ['test_data', 'auth']

    def setUp(self):
        self.client.login(username='admin', password='admin')
        self.department_list_url = reverse("api:department-list")

    def test_is_fixtures_load(self):
        """
        test load fixture with model department and auth models
        """
        self.assertTrue(Department.objects.all().exists())
        self.assertTrue(Group.objects.all().exists())
        self.assertTrue(Student.objects.all().exists())
        self.assertTrue(User.objects.all().exists())
        self.assertTrue(Group_auth.objects.all().exists())
        self.assertTrue(Permission.objects.all().exists())

    def test_get_department_list_success(self):
        """
        test api get department list success
        """
        count_dep = Department.objects.count()
        self.assertEqual(2, count_dep)
        get = self.client.get(self.department_list_url)
        self.assertEqual(get.status_code, HTTP_200_OK)
        self.assertEqual(get.data.get("status"), SUCCESS_STATUS)
        self.assertEqual(len(get.data.get("data")), count_dep)

    def test_post_department_success(self):
        """
        test api post department success
        """
        department = {
            "name_department": "department 1"
        }
        expected_response_keys = {
            "id",
            "name_department",
            "count_group",
            "count_student",
            "avg_age",
        }
        count_dep = Department.objects.count()
        post = self.client.post(self.department_list_url, department)
        self.assertEqual(post.status_code, HTTP_201_CREATED)
        self.assertEqual(post.data.get("status"), SUCCESS_STATUS)
        self.assertEqual(
            set(post.data.get("data").keys()), expected_response_keys)
        self.assertEqual(Department.objects.count(), count_dep + 1)

    def test_post_department_bad_data(self):
        """
        test api post department bad data
        """
        department = {
            "name_department": ""
        }
        count_dep = Department.objects.count()
        add = self.client.post(self.department_list_url, department)
        self.assertEqual(add.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(add.data.get("status"), FAIL_STATUS)
        self.assertEqual(Department.objects.count(), count_dep)

    def test_get_department_detail_success(self):
        """
        test api get department detail success
        """
        expected_response_keys = {
            "id",
            "name_department",
            "count_group",
            "count_student",
            "avg_age",
        }
        department = Department.objects.first()
        department_url = reverse(
            'api:department-detail', kwargs={"pk": department.id})
        get_detail = self.client.get(department_url)
        self.assertEqual(get_detail.status_code, HTTP_200_OK)
        self.assertEqual(get_detail.data.get("status"), SUCCESS_STATUS)
        self.assertEqual(
            set(get_detail.data.get("data").keys()), expected_response_keys)

    def test_put_department_fail(self):
        """
        test api put department fail
        """
        department = Department.objects.last()
        department_url = reverse(
            'api:department-detail', kwargs={"pk": department.id+1})
        get = self.client.get(department_url)
        self.assertEqual(get.status_code, HTTP_404_NOT_FOUND)
        self.assertEqual(get.data.get("status"), FAIL_STATUS)


    def test_put_department_success(self):
        """
        test api put department success
        """
        department = Department.objects.first()
        department_new = {
            "id": department.id,
            "name_department": department.name_department+"new"
        }
        expected_response_keys = {
            "id",
            "name_department",
            "count_group",
            "count_student",
            "avg_age",
        }
        department_url = reverse(
            'api:department-detail', kwargs={"pk": department.id})
        get = self.client.get(department_url)
        self.assertEqual(get.status_code, HTTP_200_OK)
        self.assertEqual(get.data.get("status"), SUCCESS_STATUS)
        put = self.client.put(department_url, department_new)
        self.assertEqual(put.status_code, HTTP_200_OK)
        self.assertEqual(put.data.get("status"), SUCCESS_STATUS)
        self.assertEqual(
            set(put.data.get("data").keys()), expected_response_keys)
        updated_department = Department.objects.get(pk=department.pk)
        self.assertNotEqual(
            department.name_department, updated_department.name_department)

    def test_put_department_bad_data(self):
        """
        test api put department bad_data
        """
        department = Department.objects.first()
        department_new = {
            "id": department.id,
            "name_department": ""
        }
        department_url = reverse(
            'api:department-detail', kwargs={"pk": department.id})
        put = self.client.put(department_url, department_new)
        self.assertEqual(put.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(put.data.get("status"), FAIL_STATUS)

    def test_delete_department_success(self):
        """
        test api delete department success
        """
        count_dep = Department.objects.count()
        delete_department = Department.objects.last()
        department_url = reverse(
            'api:department-detail', kwargs={"pk": delete_department.id})
        post = self.client.delete(department_url)
        self.assertEqual(post.status_code, HTTP_204_NO_CONTENT)
        self.assertEqual(post.data.get("status"), SUCCESS_STATUS)
        self.assertEqual(Department.objects.count(), count_dep-1)

    def test_get_age(self):
        """
        test to obtain the age of the students to calculate the average age
        """
        today = date.today()
        year = 1991

        day_before = date(year=year, month=today.month, day=today.day-1)
        day_today = date(year=year, month=today.month, day=today.day)
        day_after = date(year=year, month=today.month, day=today.day+1)

        age_full = today.year - year
        age_not_full = today.year - year - 1
        department_serializer = DepartmentSerializer()

        day_before_get = department_serializer.get_age(day_before)
        self.assertEqual(age_full, day_before_get)
        day_today_get = department_serializer.get_age(day_today)
        self.assertEqual(age_full, day_today_get)
        day_after_get = department_serializer.get_age(day_after)
        self.assertEqual(age_not_full, day_after_get)


class GroupTestCase(APITestCase):
    """
    test api group get, post, put, delete
    """
    fixtures = ['initial_data', 'auth']

    def setUp(self):
        self.client.login(username='admin', password='admin')

    def test_add_group_success(self):
        """
        test add group
        """
        group = {
            "name": "group 5",
        }
        #add = self.client.post('/api/v1/group/', group)
        #self.assertEqual(add.status_code, HTTP_201_CREATED)
        #get = self.client.get('/api/v1/group/')
        #self.assertEqual(get.status_code, HTTP_200_OK)
        #gets = get.data.get("data")
        #self.assertEqual(gets[0].get("name"), 2)
        #gg = Group.objects.get(pk=1)
        #self.assertEqual(gg.name, 2)
        #self.assertTrue(Group.objects.all().exists())