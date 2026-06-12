from rest_framework import decorators, response, serializers, status, viewsets

from trainers.models import Trainer, TrainerUnit


class TrainerUnitSerializer(serializers.ModelSerializer):
    unit_name = serializers.CharField(source="unit.name", read_only=True)
    unit_code = serializers.CharField(source="unit.code", read_only=True)

    class Meta:
        model = TrainerUnit
        fields = ["id", "unit", "unit_name", "unit_code"]


class TrainerSerializer(serializers.ModelSerializer):
    assigned_units = TrainerUnitSerializer(source="trainerunit_set", many=True, read_only=True)
    pin = serializers.CharField(write_only=True, required=False, allow_blank=False)

    class Meta:
        model = Trainer
        fields = [
            "id",
            "institution",
            "name",
            "id_number",
            "email",
            "phone",
            "photo",
            "pin",
            "is_active",
            "assigned_units",
        ]

    def create(self, validated_data):
        pin = validated_data.pop("pin", None)
        trainer = Trainer(**validated_data)
        trainer.set_pin(pin or validated_data["id_number"][-4:])
        trainer.save()
        return trainer

    def update(self, instance, validated_data):
        pin = validated_data.pop("pin", None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        if pin:
            instance.set_pin(pin)
        instance.save()
        return instance


class TrainerViewSet(viewsets.ModelViewSet):
    queryset = Trainer.objects.prefetch_related("trainerunit_set__unit").all()
    serializer_class = TrainerSerializer

    @decorators.action(detail=False, methods=["post"], url_path="verify-pin")
    def verify_pin(self, request):
        id_number = request.data.get("id_number", "").strip()
        pin = request.data.get("pin", "")
        trainer = Trainer.objects.filter(id_number=id_number, is_active=True).first()

        if not trainer or not trainer.check_pin(pin):
            return response.Response(
                {"detail": "Invalid trainer ID or PIN."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return response.Response(TrainerSerializer(trainer).data)
