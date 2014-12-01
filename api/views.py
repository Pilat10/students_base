from api.serializers import StudentSerializer, GroupSerializer, UserSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.status import HTTP_401_UNAUTHORIZED
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser
from base.models import Group, Student
from api.mixins import ResponseDataWrapperMixin
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response


class GroupListView(ResponseDataWrapperMixin, generics.ListCreateAPIView):
    """
    <pre>
    {
        "name": "group 5",
        "headman": null
    }
    </pre>
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


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
    authentication_classes = (SessionAuthentication, )
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