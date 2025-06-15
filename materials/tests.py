from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import User


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@test.com")
        self.course = Course.objects.create(
            name="test_course", description="test_description", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            name="test_lesson", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.course.name)

    def test_course_create(self):
        url = reverse("materials:course-list")
        data = {"name": "Курс1", "link": "https://www.youtube.com/s"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)

    def test_course_update(self):
        url = reverse("materials:course-detail", args=(self.course.pk,))
        data = {"name": "Курс", "link": "https://www.youtube.com/"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Курс")

    def test_course_delete(self):
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)

    def test_course_list(self):
        url = reverse("materials:course-list")
        response = self.client.get(url)
        data = response.json()
        result = data["results"]
        res = len(result[0])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(res, 6)


        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("message"), "подписка удалена")


class LessonsTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@test.com")
        self.course = Course.objects.create(
            name="test_course", description="test_description", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            name="test_lesson", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("materials:lessons-retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_lesson_create(self):
        url = reverse("materials:lessons-create")
        data = {"name": "Урок"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse("materials:lessons-update", args=(self.lesson.pk,))
        data = {"name": "Урок3"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Урок3")

    def test_lesson_delete(self):
        url = reverse("materials:lessons-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("materials:lessons-list")
        response = self.client.get(url)
        data = response.json()
        result = data["results"]
        res = len(result[0])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(res, 2)


