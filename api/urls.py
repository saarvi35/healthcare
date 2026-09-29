from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import DoctorViewSet, MappingViewSet, PatientDoctorsView, PatientViewSet, RegisterView

router = DefaultRouter()
router.register("patients", PatientViewSet, basename="patient")
router.register("doctors", DoctorViewSet, basename="doctor")
router.register("mappings", MappingViewSet, basename="mapping")

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", TokenObtainPairView.as_view(), name="login"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("mappings/<int:patient_id>/", PatientDoctorsView.as_view(), name="patient_doctors"),
    path("", include(router.urls)),
]
