from rest_framework import serializers
from base.models import Student, Group


class StudentSerializer(serializers.ModelSerializer):
    """

    """
    #group = GroupNameSerializer()

    class Meta:
        model = Student
        fields = (
            "id",
            "fio",
            "birthday",
            "number_student_cart",
            "group",
        )


class GroupSerializer(serializers.ModelSerializer):
    """

    """
    #headman = StudentFioSerializer()

    class Meta:
        model = Group
        fields = (
            "id",
            "name",
            "headman",
        )

#    def is_valid(self):
#        stud = Student.objects.get(pk=self)
#        return super(GroupSerializer, self).is_valid()