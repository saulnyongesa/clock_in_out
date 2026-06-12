from rest_framework import serializers, viewsets

from institutions.models import Institution


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = [
            "id",
            "name",
            "logo",
            "email",
            "phone",
            "address",
            "clock_out_allowance_minutes",
            "default_class_minutes",
        ]


class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
