from rest_framework.test import APITestCase
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_201_CREATED,\
    HTTP_200_OK
from django.contrib.auth.models import User

SUCCESS_STATUS = 'success'
FAIL_STATUS = 'fail'

class AuthenticationTastCase(APITestCase):
    """
    test login, logaut, authentication
    """
    def setUp(self):
        User.objects.create_user('admin', 'admin@admin.admin', 'admin')

    def test_login_fail(self):
        """
        test login fail
        """
        user = {
            "username": "fail_admin",
            "password": "admin",
        }
        login = self.client.post('/api/v1/auth/', user)
        self.assertEqual(login.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(login.data.get("status"), FAIL_STATUS)

    def test_login_success(self):
        """
        test login success
        """
        user = {
            "username": "admin",
            "password": "admin",
        }
        login = self.client.post('/api/v1/auth/', user)
        self.assertEqual(login.status_code, HTTP_200_OK)
        self.assertEqual(login.data.get("status"), SUCCESS_STATUS)

    def test_auth_success(self):
        """
        test auth success
        """
        user = {
            "username": "admin",
            "password": "admin",
        }
        self.client.post('/api/v1/auth/', user)
        auth = self.client.get('/api/v1/auth/')
        self.assertEqual(auth.status_code, HTTP_200_OK)
        self.assertEqual(auth.data.get("status"), SUCCESS_STATUS)
        data = auth.data.get("data")
        self.assertEqual(data["user"], "admin")

    def test_auth_fail(self):
        """
        test auth success
        """
        user = {
            "username": "fail_admin",
            "password": "admin",
        }
        #self.client.post('/api/v1/auth/', user)
        auth = self.client.get('/api/v1/auth/')
        self.assertEqual(auth.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(auth.data.get("status"), FAIL_STATUS)
        data = auth.data.get("data")
        self.assertEqual(data["user"], "AnonymousUser")