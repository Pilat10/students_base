from rest_framework import serializers
from base.models import Student, Group, Department
from django.contrib.auth.models import User
from datetime import date
from django.db.models import Count


class DepartmentSerializer(serializers.ModelSerializer):
    """

    """
    count_group = serializers.SerializerMethodField('count_group_fun')
    count_student = serializers.SerializerMethodField('count_student_fun')
    avg_age = serializers.SerializerMethodField('avg_age_fun')

    def count_group_fun(self, obj):
        return obj.group_set.count()

    def count_student_fun(self, obj):
        count_student = Department.objects.annotate(
            count_stud=Count('group__student')).get(pk=obj.pk)
        return count_student.count_stud

    def avg_age_fun(self, obj):
        count_student = self.count_student_fun(obj)
        if count_student:
            students = Student.objects.filter(group__department__pk=obj.pk)
            count_year = 0
            for student in students:
                count_year += self.get_age(student.birthday)
            return float(count_year)/float(count_student)
        else:
            return 0

    def get_age(self, birthday):
        today = date.today()
        birth_day = birthday - date(year=birthday.year, month=1, day=1)
        today_day = today - date(year=today.year, month=1, day=1)
        if birth_day <= today_day:
            return today.year - birthday.year
        else:
            return today.year - birthday.year - 1


    class Meta:
        model = Department
        fields = (
            "id",
            "name_department",
            "count_group",
            "count_student",
            "avg_age",
        )


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
    count_student = serializers.SerializerMethodField('count_student_fun')
    headman_name = serializers.SerializerMethodField('headman_name_fun')

    def count_student_fun(self, obj):
        return obj.student_set.count()

    def headman_name_fun(self, obj):
        return obj.headman

    class Meta:
        model = Group
        fields = (
            "id",
            "name",
            "department",
            "count_student",
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