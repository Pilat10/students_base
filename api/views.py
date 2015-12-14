from api.serializers import StudentSerializer, GroupSerializer, \
    UserSerializer, DepartmentSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.status import HTTP_401_UNAUTHORIZED
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser
from base.models import Group, Student, Department
from api.mixins import ResponseDataWrapperMixin, \
    ResponseDataWrapperMixinSuccess
# from rest_framework.authentication import SessionAuthentication, \
# TokenAuthentication
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


class DepartmentListView(ResponseDataWrapperMixin, generics.ListCreateAPIView):
    """
    <pre>
    {
        "name_department": "dep 3"
    }
    </pre>
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class DepartmentDetailView(ResponseDataWrapperMixin,
                           generics.RetrieveUpdateDestroyAPIView):
    """

    """
    model = Department
    serializer_class = DepartmentSerializer


class GroupListView(ResponseDataWrapperMixin, generics.ListCreateAPIView):
    """
    <pre>
    {
        "name": "group 5",
        "department": 1,
        "headman": null
    }
    </pre>
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get_queryset(self):
        department_id = self.request.QUERY_PARAMS.get('department_id', None)
        if department_id is not None:
            return super(GroupListView, self).get_queryset().filter(
                department__pk=department_id)
        return super(GroupListView, self).get_queryset()


class GroupDetailView(ResponseDataWrapperMixin,
                  generics.RetrieveUpdateDestroyAPIView):
    """

    """
    model = Group
    serializer_class = GroupSerializer


class StudentListView(ResponseDataWrapperMixin, generics.ListCreateAPIView):
    """

    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_queryset(self):
        group_id = self.request.QUERY_PARAMS.get('group_id', None)
        if group_id is not None:
            return super(StudentListView, self).get_queryset().filter(
                group__pk=group_id)
        return super(StudentListView, self).get_queryset()


class StudentDetailView(ResponseDataWrapperMixin,
                    generics.RetrieveUpdateDestroyAPIView):
    """

    """
    model = Student
    serializer_class = StudentSerializer


class LoginView(ResponseDataWrapperMixin, APIView):
    """
    <pre>
        {
         "username": "admin",
         "password": "admin"
        }
    </pre>
    """
    # authentication_classes = (SessionAuthentication, )
    permission_classes = ()

    def credentials(self, request):
        username = request.DATA.get("username")
        password = request.DATA.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return user
        return None

    def post(self, request):
        #username = request.DATA.get("username")
        user = self.credentials(request)
        if not user:
            return Response(
                {"error": "wrong username or password"}, HTTP_401_UNAUTHORIZED)
        login(request, user)
        return Response(
            {"user": UserSerializer(user, context={"request": request}).data})

    def get(self, request, format=None):
        content = {
            'user': unicode(request.user),
            'auth': unicode(request.auth),
        }
        if (request.user == AnonymousUser()):
            return Response(content, HTTP_401_UNAUTHORIZED)
        return Response(content)

    def delete(self, request):
        logout(request)
        return Response({})


class LoginTokenView(ResponseDataWrapperMixinSuccess, APIView):
    """
    <pre>
        {
         "username": "admin",
         "password": "admin"
        }
    </pre>
    """
    authentication_classes = ()
    permission_classes = ()

    def credentials(self, request):
        username = request.DATA.get("username")
        password = request.DATA.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return user
        return None

    def post(self, request):
        user = self.credentials(request)
        if not user:
            return Response(
                {"error": "wrong username or password"}, HTTP_401_UNAUTHORIZED)
        token = Token.objects.create(user)
        # login(request, user)
        return Response(
            {
                "token": token.key,
                "user": UserSerializer(user, context={"request": request}).data
            })

    def get(self, request, format=None):
        content = {
            'user': unicode(request.user),
            'auth': unicode(request.auth),
        }
        if (request.user == AnonymousUser()):
            return Response(content, HTTP_401_UNAUTHORIZED)
        return Response(content)

    def delete(self, request):
        logout(request)
        return Response({})
