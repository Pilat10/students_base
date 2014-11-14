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
    count = serializers.SerializerMethodField('count_student')
    headman_name = serializers.SerializerMethodField('headman_name_fun')

    def count_student(self, obj):
        return obj.student_set.count()

    def headman_name_fun(self, obj):
        return obj.headman

    class Meta:
        model = Group
        fields = (
            "id",
            "name",
            "count",
            "headman",
            "headman_name"
        )

#    def is_valid(self):
#        stud = Student.objects.get(pk=self)
#        return super(GroupSerializer, self).is_valid()