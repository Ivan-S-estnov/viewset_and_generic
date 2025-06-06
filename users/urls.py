from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.apps import UsersConfig
from users.views import (PaymentViewSet, PaymentCreateApiView, PaymentListApiView, PaymentRetrieveApiView,
                            PaymentUpdateApiView, PaymentDestroyApiView, UserCreateApiView)

app_name = UsersConfig.name

router = SimpleRouter()
router.register("", PaymentViewSet)

urlpatterns = [
    path("payment/", PaymentListApiView.as_view(), name="payment_list"),
    path("payment/<int:pk>/", PaymentRetrieveApiView.as_view(), name="payment_retrieve"),
    path("payment/create/", PaymentCreateApiView.as_view(), name="payment_create"),
    path(
        "payment/<int:pk>/delete/", PaymentDestroyApiView.as_view(), name="payment_delete"
    ),
    path(
        "payment/<int:pk>/update/", PaymentUpdateApiView.as_view(), name="payment_update"
    ),
    path("register/", UserCreateApiView.as_view(), name="register"),
    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls
