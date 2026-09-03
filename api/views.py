import csv

from api.serializers import StudentSerializer, GroupSerializer, \
    UserSerializer, DepartmentSerializer
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.status import HTTP_401_UNAUTHORIZED
from django.contrib.auth import authenticate, login, logout
from base.models import Group, Student, Department
from api.mixins import ResponseDataWrapperMixin, \
    ResponseDataWrapperMixinSuccess
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError


def filter_students_by_name(queryset, query_params):
    search_term = query_params.get("q", "").strip()
    if not search_term:
        return queryset
    return queryset.filter(fio__icontains=search_term)


def filter_students(queryset, query_params):
    """
    Shared by StudentListView and StudentExportView so the CSV export
    always matches whatever group_id/department_id/q filters are applied
    to the JSON list.
    """
    group_id = query_params.get('group_id', None)
    if group_id is not None:
        queryset = queryset.filter(group__pk=group_id)
    department_id = query_params.get('department_id', None)
    if department_id is not None:
        queryset = queryset.filter(group__department__pk=department_id)
    return filter_students_by_name(queryset, query_params)


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
    queryset = Department.objects.all()
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
        queryset = super().get_queryset()
        department_id = self.request.query_params.get('department_id', None)
        if department_id is not None:
            queryset = queryset.filter(
                department__pk=department_id)

        has_headman = self.request.query_params.get('has_headman', None)
        if has_headman is None:
            return queryset

        has_headman = has_headman.strip().lower()
        if has_headman == 'true':
            return queryset.exclude(headman=None)
        if has_headman == 'false':
            return queryset.filter(headman=None)
        raise ValidationError({
            'has_headman': 'Expected "true" or "false".',
        })


class GroupDetailView(ResponseDataWrapperMixin,
                  generics.RetrieveUpdateDestroyAPIView):
    """

    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class StudentListView(ResponseDataWrapperMixin, generics.ListCreateAPIView):
    """

    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return filter_students(queryset, self.request.query_params)


class StudentDetailView(ResponseDataWrapperMixin,
                    generics.RetrieveUpdateDestroyAPIView):
    """

    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentExportView(APIView):
    """
    Exports students as CSV, honoring the same group_id/department_id/q
    filters as StudentListView. Not wrapped in ResponseDataWrapperMixin:
    the response body is CSV, not JSON, so the {status, data} envelope
    doesn't apply.
    """

    def get(self, request):
        queryset = filter_students(
            Student.objects.select_related('group__department'),
            request.query_params)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = \
            'attachment; filename="students.csv"'

        writer = csv.writer(response)
        writer.writerow(
            ['fio', 'birthday', 'number_student_cart', 'group', 'department'])
        for student in queryset:
            writer.writerow([
                student.fio,
                student.birthday,
                student.number_student_cart,
                student.group.name,
                student.group.department.name_department,
            ])
        return response


class BaseLoginView(APIView):
    """
    <pre>
        {
         "username": "admin",
         "password": "admin"
        }
    </pre>
    """
    permission_classes = ()

    def credentials(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            return user
        return None

    def get(self, request, format=None):
        content = {
            'user': str(request.user),
            'auth': str(request.auth),
        }
        if not request.user.is_authenticated:
            return Response(content, HTTP_401_UNAUTHORIZED)
        return Response(content)

    def delete(self, request):
        logout(request)
        return Response({})


class LoginView(ResponseDataWrapperMixin, BaseLoginView):

    def post(self, request):
        user = self.credentials(request)
        if not user:
            return Response(
                {"error": "wrong username or password"}, HTTP_401_UNAUTHORIZED)
        login(request, user)
        return Response(
            {"user": UserSerializer(user, context={"request": request}).data})


class LoginTokenView(ResponseDataWrapperMixinSuccess, BaseLoginView):
    authentication_classes = ()

    def post(self, request):
        user = self.credentials(request)
        if not user:
            return Response(
                {"error": "wrong username or password"}, HTTP_401_UNAUTHORIZED)
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user": UserSerializer(user, context={"request": request}).data
            })
