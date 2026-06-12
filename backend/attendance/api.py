from django.db.models import Sum
from rest_framework import decorators, response, serializers, status, viewsets

from academics.models import Unit
from attendance.models import AttendanceSession
from trainers.models import Trainer


class AttendanceSessionSerializer(serializers.ModelSerializer):
    trainer_name = serializers.CharField(source="trainer.name", read_only=True)
    unit_name = serializers.CharField(source="unit.name", read_only=True)
    unit_code = serializers.CharField(source="unit.code", read_only=True)

    class Meta:
        model = AttendanceSession
        fields = [
            "id",
            "institution",
            "trainer",
            "trainer_name",
            "unit",
            "unit_name",
            "unit_code",
            "clock_in_at",
            "clock_out_at",
            "actual_minutes",
            "credited_minutes",
            "roll",
            "clock_in_photo",
            "clock_out_photo",
            "is_active",
        ]
        read_only_fields = ["institution", "actual_minutes", "credited_minutes", "is_active"]


class AttendanceSessionViewSet(viewsets.ModelViewSet):
    queryset = AttendanceSession.objects.select_related("institution", "trainer", "unit").all()
    serializer_class = AttendanceSessionSerializer

    @decorators.action(detail=False, methods=["get"], url_path="active-for-trainer/(?P<trainer_id>[^/.]+)")
    def active_for_trainer(self, request, trainer_id=None):
        session = self.queryset.filter(trainer_id=trainer_id, is_active=True).first()
        if not session:
            return response.Response({"active_session": None})
        return response.Response({"active_session": AttendanceSessionSerializer(session).data})

    @decorators.action(detail=False, methods=["post"], url_path="clock-in")
    def clock_in(self, request):
        trainer = Trainer.objects.filter(id=request.data.get("trainer")).first()
        if not trainer:
            return response.Response({"detail": "Trainer not found."}, status=status.HTTP_404_NOT_FOUND)
        if "clock_in_photo" not in request.FILES:
            return response.Response(
                {"detail": "Clock-in camera snapshot is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        active = AttendanceSession.objects.filter(trainer=trainer, is_active=True).first()
        if active:
            return response.Response(
                {"detail": "Trainer is already clocked in.", "active_session": AttendanceSessionSerializer(active).data},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = AttendanceSessionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(institution=trainer.institution, trainer=trainer)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)

    @decorators.action(detail=True, methods=["post"], url_path="clock-out")
    def clock_out(self, request, pk=None):
        session = self.get_object()
        if not session.is_active:
            return response.Response({"detail": "Session is already clocked out."}, status=status.HTTP_400_BAD_REQUEST)
        if "clock_out_photo" not in request.FILES:
            return response.Response(
                {"detail": "Clock-out camera snapshot is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        session.roll = request.data.get("roll", session.roll)
        session.clock_out_photo = request.FILES["clock_out_photo"]
        session.clock_out()
        session.save()
        return response.Response(AttendanceSessionSerializer(session).data)

    @decorators.action(detail=False, methods=["get"], url_path="unit-stats/(?P<trainer_id>[^/.]+)/(?P<unit_id>[^/.]+)")
    def unit_stats(self, request, trainer_id=None, unit_id=None):
        sessions = self.queryset.filter(trainer_id=trainer_id, unit_id=unit_id, is_active=False)
        credited_minutes = sessions.aggregate(total=Sum("credited_minutes"))["total"] or 0
        credited_hours = round(credited_minutes / 60, 2)
        unit = Unit.objects.filter(id=unit_id).first()

        target = float(unit.term_hours_target) if unit else 0
        remaining = max(0, round(target - credited_hours, 2))
        progress = round((credited_hours / target) * 100, 1) if target else 0

        return response.Response(
            {
                "credited_hours": credited_hours,
                "term_target_hours": target,
                "remaining_hours": remaining,
                "progress_percent": min(progress, 100),
            }
        )
