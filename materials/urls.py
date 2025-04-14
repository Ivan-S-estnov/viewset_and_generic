from rest_framework.routers import SimpleRouter
from materials.apps import MaterialsConfig
from materials.views import *
from django.urls import path
app_name = MaterialsConfig.name

router = SimpleRouter()
router.register("",LessonViewSet)

urlpatterns = [
    path("courses/", CourseListApiView.as_view(), name='course_list'),
    path("courses/<int:pk>", CourseRetrieveApiView.as_view(), name='course_retrieve'),
    path("courses/create/", CourseCreateApiView.as_view(), name='course_create'),
    path("courses/<int:pk>/delete/", CourseDestroyApiView.as_view(), name='course_delete'),
    path("courses/<int:pk>/update/", CourseUpdateApiView.as_view(), name='course_update'),

]

urlpatterns += router.urls