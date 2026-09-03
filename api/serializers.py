from rest_framework import serializers
from base.models import Student, Group, Department
from django.contrib.auth.models import User
from datetime import date


class DepartmentSerializer(serializers.ModelSerializer):
    """

    """
    count_group = serializers.SerializerMethodField()
    count_student = serializers.SerializerMethodField()
    avg_age = serializers.SerializerMethodField()

    def get_count_group(self, obj):
        return obj.group_set.count()

    def get_count_student(self, obj):
        return Student.objects.filter(group__department=obj).count()

    def get_avg_age(self, obj):
        count_student = self.get_count_student(obj)
        if count_student:
            students = Student.objects.filter(group__department__pk=obj.pk)
            count_year = 0
            for student in students:
                count_year += self.get_age(student.birthday)
            return int(float(count_year)/float(count_student))
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


class EmptyStringAsNullPKField(serializers.PrimaryKeyRelatedField):
    """
    The AngularJS SPA sends `"headman": ''` to mean "no headman". DRF 2
    coerced that to None; DRF 3's PrimaryKeyRelatedField rejects it. This
    only matters for JSON input (DRF's built-in ''->None rule already
    covers form-encoded input via Field.get_value()).
    """

    def to_internal_value(self, data):
        if data == '' or data is None:
            return None
        return super().to_internal_value(data)


class GroupSerializer(serializers.ModelSerializer):
    """

    """
    count_student = serializers.SerializerMethodField()
    headman_name = serializers.SerializerMethodField()
    has_headman = serializers.SerializerMethodField()
    headman = EmptyStringAsNullPKField(
        queryset=Student.objects.all(), allow_null=True, required=False)

    def get_count_student(self, obj):
        return obj.student_set.count()

    def get_headman_name(self, obj):
        return str(obj.headman) if obj.headman_id else None

    def get_has_headman(self, obj):
        return obj.headman_id is not None

    class Meta:
        model = Group
        fields = (
            "id",
            "name",
            "department",
            "count_student",
            "headman",
            "headman_name",
            "has_headman",
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
