from rest_framework import permissions, serializers, viewsets

from academics.models import Unit


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = [
            "id",
            "institution",
            "code",
            "name",
            "class_minutes",
            "weekly_hours_target",
            "term_hours_target",
            "is_active",
        ]


class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.select_related("institution").all()
    serializer_class = UnitSerializer
    permission_classes = [permissions.AllowAny]
