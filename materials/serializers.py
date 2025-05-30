from rest_framework.serializers import ModelSerializer
from rest_framework.fields import SerializerMethodField
from materials.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True)
    class Meta:
        model = Course
        fields = "__all__"

class CourseDetailSerializer(ModelSerializer):
    count_lessons = SerializerMethodField()
    lessons = LessonSerializer(many=True)

    def get_count_lessons(self, course):
        return Lesson.objects.filter(course=course.lessons).count()

    class Meta:
        model = Course
        fields = ("name", "description", "count_lessons", "lessons")
