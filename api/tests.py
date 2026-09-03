from datetime import date, timedelta

from rest_framework.test import APITestCase
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
)
from django.contrib.auth.models import User, Group as Group_auth, Permission
from api.serializers import DepartmentSerializer
from base.models import Department, Group, Student
from django.urls import reverse

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
        test load fixture with model department, group, student and auth models
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

        day_today = date(year, 1, 1) + (today - date(today.year, 1, 1))
        day_before = day_today - timedelta(days=1)
        day_after = day_today + timedelta(days=1)

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
    fixtures = ['test_data', 'auth']

    def setUp(self):
        self.client.login(username='admin', password='admin')
        self.group_list_url = reverse("api:group-list")
        self.expected_response_keys = {
            "id",
            "name",
            "department",
            "count_student",
            "headman",
            "headman_name",
            "has_headman",
        }

    def test_is_fixtures_load(self):
        """
        test load fixture with model department, group, student and auth models
        """
        self.assertTrue(Department.objects.all().exists())
        self.assertTrue(Group.objects.all().exists())
        self.assertTrue(Student.objects.all().exists())
        self.assertTrue(User.objects.all().exists())
        self.assertTrue(Group_auth.objects.all().exists())
        self.assertTrue(Permission.objects.all().exists())

    def test_get_group_list_success(self):
        """
        test api get group list success
        """
        count_group = Group.objects.count()
        self.assertEqual(5, count_group)
        get = self.client.get(self.group_list_url)
        self.assertEqual(get.status_code, HTTP_200_OK)
        self.assertEqual(get.data.get("status"), SUCCESS_STATUS)
        self.assertEqual(len(get.data.get("data")), count_group)

    def test_get_group_list_filters_groups_with_headman(self):
        expected_count = Group.objects.exclude(headman=None).count()
        get = self.client.get(
            self.group_list_url, {"has_headman": "true"})

        self.assertEqual(get.status_code, HTTP_200_OK)
        self.assertEqual(get.data.get("status"), SUCCESS_STATUS)
        self.assertEqual(len(get.data.get("data")), expected_count)
        self.assertTrue(
            all(group["has_headman"] for group in get.data.get("data")))

    def test_get_group_list_filters_groups_without_headman(self):
        expected_count = Group.objects.filter(headman=None).count()
        get = self.client.get(
            self.group_list_url, {"has_headman": "false"})

        self.assertEqual(get.status_code, HTTP_200_OK)
        self.assertEqual(get.data.get("status"), SUCCESS_STATUS)
        self.assertEqual(len(get.data.get("data")), expected_count)
        self.assertTrue(
            all(not group["has_headman"] for group in get.data.get("data")))

    def test_get_group_list_rejects_invalid_has_headman(self):
        get = self.client.get(
            self.group_list_url, {"has_headman": "unknown"})

        self.assertEqual(get.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(get.data.get("status"), FAIL_STATUS)
        self.assertEqual(
            set(get.data.get("data").keys()), {"has_headman", })

    def test_post_group_success(self):
        """
        test api post group success
        """
        group = {
            "name": "test group 1",
            "department": 1,
        }
        count_group = Group.objects.count()
        post = self.client.post(self.group_list_url, group)
        self.assertEqual(post.status_code, HTTP_201_CREATED)
        self.assertEqual(post.data.get("status"), SUCCESS_STATUS)
        self.assertEqual(
            set(post.data.get("data").keys()), self.expected_response_keys)
        self.assertEqual(Group.objects.count(), count_group + 1)

    def test_post_group_bad_data(self):
        """
        test api post group bad data
        """
        group = {
            "name": "test group 1",
            "department": Department.objects.last().pk + 1,
        }
        count_group = Group.objects.count()
        add = self.client.post(self.group_list_url, group)
        self.assertEqual(add.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(add.data.get("status"), FAIL_STATUS)
        self.assertEqual(Group.objects.count(), count_group)
        self.assertEqual(
            set(add.data.get("data").keys()), {"department", })

    def test_get_group_detail_success(self):
        """
        test api get group detail success
        """
        group = Group.objects.first()
        group_url = reverse(
            'api:group-detail', kwargs={"pk": group.id})
        get_detail = self.client.get(group_url)
        self.assertEqual(get_detail.status_code, HTTP_200_OK)
        self.assertEqual(get_detail.data.get("status"), SUCCESS_STATUS)
        self.assertEqual(
            set(get_detail.data.get("data").keys()), self.expected_response_keys)

    def test_put_group_fail(self):
        """
        test api put group fail
        """
        group = Group.objects.last()
        group_url = reverse(
            'api:group-detail', kwargs={"pk": group.id+1})
        get = self.client.get(group_url)
        self.assertEqual(get.status_code, HTTP_404_NOT_FOUND)
        self.assertEqual(get.data.get("status"), FAIL_STATUS)


    def test_put_group_success(self):
        """
        test api put group success
        """
        group = Group.objects.first()
        department = Department.objects.first()
        if department == group.department:
            department = Department.objects.last()
        headman = Student.objects.filter(group=group.id).first()
        if headman == group.headman:
            headman = Student.objects.filter(group=group.id).last()

        group_new = {
            "id": group.id,
            "name": group.name+"new",
            "department": department.id,
            "headman": headman.id,
        }
        group_url = reverse(
            'api:group-detail', kwargs={"pk": group.id})
        get = self.client.get(group_url)
        self.assertEqual(get.status_code, HTTP_200_OK)
        self.assertEqual(get.data.get("status"), SUCCESS_STATUS)
        put = self.client.put(group_url, group_new)
        self.assertEqual(put.status_code, HTTP_200_OK)
        self.assertEqual(put.data.get("status"), SUCCESS_STATUS)
        self.assertEqual(
            set(put.data.get("data").keys()), self.expected_response_keys)
        updated_group = Group.objects.get(pk=group.pk)
        self.assertNotEqual(
            group.name, updated_group.name)
        if department != group.department:
            self.assertNotEqual(group.department, updated_group.department)
        if headman != group.headman:
            self.assertNotEqual(group.headman, updated_group.headman)

    def test_put_group_bad_data(self):
        """
        test api put group bad_data
        """
        group = Group.objects.first()
        if group.headman is not None:
            headman = group.headman.id
        else:
            # Django's multipart test-client encoder can't encode None;
            # '' is the wire value the AngularJS SPA sends for "no headman"
            # anyway (see EmptyStringAsNullPKField in api/serializers.py).
            headman = ''
        group_new = {
            "id": group.id,
            "name": "",
            "department": group.department.id,
            "headman": headman
        }
        group_url = reverse(
            'api:group-detail', kwargs={"pk": group.id})
        put = self.client.put(group_url, group_new)
        self.assertEqual(put.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(put.data.get("status"), FAIL_STATUS)
        self.assertEqual(
            set(put.data.get("data").keys()), {"name", })


    def test_delete_group_success(self):
        """
        test api delete group success
        """
        count_group = Group.objects.count()
        delete_group = Group.objects.last()
        group_url = reverse(
            'api:group-detail', kwargs={"pk": delete_group.id})
        post = self.client.delete(group_url)
        self.assertEqual(post.status_code, HTTP_204_NO_CONTENT)
        self.assertEqual(post.data.get("status"), SUCCESS_STATUS)
        self.assertEqual(Group.objects.count(), count_group-1)

    def test_put_group_empty_headman_is_null(self):
        """
        The AngularJS SPA sends headman='' to mean "no headman" (DRF2
        coerced '' -> None; DRF3's PrimaryKeyRelatedField needs help).
        """
        group = Group.objects.exclude(headman=None).first()
        group_url = reverse('api:group-detail', kwargs={"pk": group.pk})
        put = self.client.put(group_url, {
            "name": group.name,
            "department": group.department_id,
            "headman": "",
        }, format='json')
        self.assertEqual(put.status_code, HTTP_200_OK)
        self.assertIsNone(Group.objects.get(pk=group.pk).headman)
