from rest_framework import serializers
from base.models import Student, Group
from django.contrib.auth.models import User


class StudentSerializer(serializers.ModelSerializer):
    """

    """
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


class UserSerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
        )