from rest_framework import generics, permissions, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Doctor, Patient, PatientDoctorMapping
from .serializers import (
    DoctorSerializer, PatientDoctorMappingSerializer, PatientSerializer, RegisterSerializer,
)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer

    def get_queryset(self):
        return Patient.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class MappingViewSet(viewsets.ModelViewSet):
    serializer_class = PatientDoctorMappingSerializer
    http_method_names = ["get", "post", "delete", "head", "options"]

    def get_queryset(self):
        queryset = PatientDoctorMapping.objects.filter(patient__user=self.request.user)
        patient_id = self.request.query_params.get("patient_id")
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        return queryset

    def perform_create(self, serializer):
        patient = serializer.validated_data["patient"]
        if patient.user_id != self.request.user.id:
            raise ValidationError({"patient": "Patient not found."})
        serializer.save()


class PatientDoctorsView(APIView):
    def get(self, request, patient_id):
        mappings = PatientDoctorMapping.objects.filter(
            patient_id=patient_id, patient__user=request.user
        )
        doctors = Doctor.objects.filter(patient_mappings__in=mappings).distinct()
        return Response(DoctorSerializer(doctors, many=True).data)

    def delete(self, request, patient_id):
        mapping = PatientDoctorMapping.objects.filter(
            id=patient_id, patient__user=request.user
        ).first()
        if mapping is None:
            from rest_framework.exceptions import NotFound
            raise NotFound("Mapping not found.")
        mapping.delete()
        return Response(status=204)
