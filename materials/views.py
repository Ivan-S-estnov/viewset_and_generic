from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from materials.tasks import send_mail_update_course
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from materials.paginators import CustomPagination
from rest_framework.viewsets import ModelViewSet
from users.permissions import IsModerator, IsOwner
from materials.models import Course, Lesson, Subscription
from materials.serializers import (
    CourseSerializer,
    LessonSerializer,
    SerializerMethodField,
    SubscriptionSerializer,
)
from rest_framework.response import Response
from rest_framework import status


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModerator, IsAuthenticated)
        elif self.action in ["update", "retrieve", "list"]:
            self.permission_classes = (IsModerator | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (
                IsAuthenticated,
                ~IsModerator | IsOwner,
            )
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SerializerMethodField
        return CourseSerializer


class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        lesson = serializer.save()
        courses_object_list = list(Course.objects.filter(owner=self.request.user))
        courses_list = []
        for course in courses_object_list:
            courses_list.append(course.id)
        if lesson.course.id not in courses_list:
            raise ValidationError(
                f"Вы не являетесь владельцем курса {lesson.course.name}!"
            )
        lesson.save()

    permission_classes = [IsOwner]


class LessonListApiView(ListAPIView):
    def get_queryset(self):
        if IsModerator().has_permission(self.request, self):
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=self.request.user)

    serializer_class = LessonSerializer
    pagination_class = CustomPagination


class LessonRetrieveApiView(RetrieveAPIView):
    def get_queryset(self):
        if IsModerator().has_permission(self.request, self):
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=self.request.user)

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateApiView(UpdateAPIView):
    def get_queryset(self):
        if IsModerator().has_permission(self.request, self):
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=self.request.user)

    def perform_update(self, serializer):
        lesson = serializer.save()
        courses_object_list = list(Course.objects.filter(owner=self.request.user))
        courses_list = []
        for course in courses_object_list:
            courses_list.append(course.id)
        if lesson.course.id not in courses_list:
            raise ValidationError(
                f"Вы не являетесь владельцем курса {lesson.course.name}!"
            )
        lesson.save()

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonDestroyApiView(DestroyAPIView):
    def get_queryset(self):
        if IsModerator().has_permission(self.request, self):
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=self.request.user)

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | ~IsModerator]


class SubscriptionAPIView(APIView):
    serializer_class = SubscriptionSerializer

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course")
        course = get_object_or_404(Course, pk=course_id)
        subs_item = Subscription.objects.all().filter(user=user).filter(course=course)
        send_mail_update_course.delay(course.id)
        if subs_item.exists():
            subs_item.delete()
            message = "Подписка отключена"
        else:
            Subscription.objects.create(user=user, course=course)
            message = "Подписка включена"
        return Response({"message": message}, status=status.HTTP_201_CREATED)
