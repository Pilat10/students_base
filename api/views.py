from api.serializers import StudentSerializer, GroupSerializer
from rest_framework import generics
from base.models import Group, Student
from api.mixins import ResponseDataWrapperMixin
from rest_framework import permissions


class GroupList(ResponseDataWrapperMixin, generics.ListCreateAPIView):
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
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class GroupDetail(ResponseDataWrapperMixin,
                  generics.RetrieveUpdateDestroyAPIView):
    """

    """
    model = Group
    serializer_class = GroupSerializer
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly, )



class StudentList(ResponseDataWrapperMixin, generics.ListCreateAPIView):
    """

    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        group_id = self.request.QUERY_PARAMS.get('group_id', None)
        if group_id is not None:
            return super(StudentList, self).get_queryset().filter(
                group__pk=group_id)
        return super(StudentList, self).get_queryset()


class StudentDetail(ResponseDataWrapperMixin,
                    generics.RetrieveUpdateDestroyAPIView):
    """

    """
    model = Student
    serializer_class = StudentSerializer
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly, )