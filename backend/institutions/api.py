from rest_framework import decorators, permissions, response, serializers, status, viewsets
from rest_framework.decorators import api_view, permission_classes

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

    @decorators.action(
        detail=False,
        methods=["get", "post"],
        permission_classes=[permissions.AllowAny],
        url_path="current",
    )
    def current(self, request):
        institution = Institution.objects.order_by("id").first()

        if request.method == "GET":
            if institution is None:
                return response.Response(
                    {
                        "id": None,
                        "name": "",
                        "logo": None,
                        "email": "",
                        "phone": "",
                        "address": "",
                        "clock_out_allowance_minutes": 10,
                        "default_class_minutes": 60,
                    }
                )
            return response.Response(self.get_serializer(institution).data)

        serializer = self.get_serializer(
            institution,
            data=request.data,
            partial=institution is not None,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
@permission_classes([permissions.AllowAny])
def current_institution(request):
    institution = Institution.objects.order_by("id").first()

    if request.method == "GET":
        if institution is None:
            return response.Response(
                {
                    "id": None,
                    "name": "",
                    "logo": None,
                    "email": "",
                    "phone": "",
                    "address": "",
                    "clock_out_allowance_minutes": 10,
                    "default_class_minutes": 60,
                }
            )
        return response.Response(InstitutionSerializer(institution).data)

    serializer = InstitutionSerializer(
        institution,
        data=request.data,
        partial=institution is not None,
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return response.Response(serializer.data, status=status.HTTP_200_OK)
