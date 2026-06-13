from pathlib import Path

from django.core.files.storage import default_storage
from PIL import Image, ImageOps
from rest_framework import decorators, permissions, response, serializers, status, viewsets

from trainers.models import Trainer, TrainerUnit


def _hamming_distance(left, right):
    return sum(1 for left_bit, right_bit in zip(left, right) if left_bit != right_bit)


def _average_hash(image):
    small = ImageOps.grayscale(image).resize((8, 8))
    pixels = list(small.getdata())
    average = sum(pixels) / len(pixels)
    return [pixel >= average for pixel in pixels]


def _difference_hash(image):
    small = ImageOps.grayscale(image).resize((9, 8))
    pixels = list(small.getdata())
    bits = []
    for row in range(8):
        start = row * 9
        for column in range(8):
            bits.append(pixels[start + column] > pixels[start + column + 1])
    return bits


def _histogram_similarity(left, right):
    left_histogram = ImageOps.grayscale(left).resize((96, 96)).histogram()
    right_histogram = ImageOps.grayscale(right).resize((96, 96)).histogram()
    intersection = sum(min(left_value, right_value) for left_value, right_value in zip(left_histogram, right_histogram))
    total = max(sum(left_histogram), sum(right_histogram), 1)
    return intersection / total


def lightweight_photo_verify(snapshot_path, reference_path):
    """Pillow-only fallback used when DeepFace/TensorFlow is unavailable."""
    with Image.open(snapshot_path) as snapshot_image, Image.open(reference_path) as reference_image:
        snapshot = ImageOps.exif_transpose(snapshot_image).convert("RGB")
        reference = ImageOps.exif_transpose(reference_image).convert("RGB")
        average_similarity = 1 - (_hamming_distance(_average_hash(snapshot), _average_hash(reference)) / 64)
        difference_similarity = 1 - (_hamming_distance(_difference_hash(snapshot), _difference_hash(reference)) / 64)
        histogram_score = _histogram_similarity(snapshot, reference)

    score = round((average_similarity * 0.35) + (difference_similarity * 0.35) + (histogram_score * 0.30), 4)
    return {
        "verified": score >= 0.62,
        "distance": round(1 - score, 4),
        "model": "pillow-lightweight",
        "score": score,
    }


class TrainerUnitSerializer(serializers.ModelSerializer):
    unit_name = serializers.CharField(source="unit.name", read_only=True)
    unit_code = serializers.CharField(source="unit.code", read_only=True)

    class Meta:
        model = TrainerUnit
        fields = ["id", "unit", "unit_name", "unit_code"]


class TrainerSerializer(serializers.ModelSerializer):
    assigned_units = TrainerUnitSerializer(source="trainerunit_set", many=True, read_only=True)

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
            "is_active",
            "assigned_units",
        ]

    def validate(self, attrs):
        if self.instance is None and not attrs.get("photo"):
            raise serializers.ValidationError(
                {"photo": "Reference photo is required for face verification."}
            )
        return attrs


class TrainerViewSet(viewsets.ModelViewSet):
    queryset = Trainer.objects.prefetch_related("trainerunit_set__unit").all()
    serializer_class = TrainerSerializer
    permission_classes = [permissions.AllowAny]

    @decorators.action(detail=True, methods=["post"], url_path="assign-unit")
    def assign_unit(self, request, pk=None):
        trainer = self.get_object()
        unit_id = request.data.get("unit")
        if not unit_id:
            return response.Response(
                {"detail": "Unit is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        assignment, _ = TrainerUnit.objects.get_or_create(
            trainer=trainer,
            unit_id=unit_id,
        )
        return response.Response(TrainerUnitSerializer(assignment).data)

    @decorators.action(detail=True, methods=["post"], url_path="remove-unit")
    def remove_unit(self, request, pk=None):
        trainer = self.get_object()
        unit_id = request.data.get("unit")
        TrainerUnit.objects.filter(trainer=trainer, unit_id=unit_id).delete()
        return response.Response({"removed": True})

    @decorators.action(detail=False, methods=["post"], url_path="verify-face")
    def verify_face(self, request):
        id_number = request.data.get("id_number", "").strip()
        snapshot = request.FILES.get("snapshot")
        trainer = Trainer.objects.filter(id_number=id_number, is_active=True).first()

        if not trainer:
            return response.Response(
                {"detail": "Trainer not found or inactive."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not trainer.photo:
            return response.Response(
                {"detail": "Trainer has no registered reference photo."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not snapshot:
            return response.Response(
                {"detail": "Live camera snapshot is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        temp_name = None
        try:
            temp_name = default_storage.save(f"face_checks/{snapshot.name}", snapshot)
            snapshot_path = Path(default_storage.path(temp_name))
            reference_path = Path(trainer.photo.path)

            try:
                from deepface import DeepFace

                result = DeepFace.verify(
                    img1_path=str(snapshot_path),
                    img2_path=str(reference_path),
                    model_name="Facenet",
                    detector_backend="opencv",
                    enforce_detection=True,
                )
                result["model"] = "deepface-facenet"
            except ImportError:
                result = lightweight_photo_verify(snapshot_path, reference_path)
        except ImportError:
            return response.Response(
                {"detail": "DeepFace is not installed on this backend."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        except Exception as exc:
            return response.Response(
                {"detail": f"Face verification failed: {exc}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        finally:
            if temp_name:
                default_storage.delete(temp_name)

        if not result.get("verified"):
            return response.Response(
                {
                    "detail": "Face did not match the registered trainer photo.",
                    "distance": result.get("distance"),
                    "model": result.get("model"),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return response.Response(
            {
                "verified": True,
                "distance": result.get("distance"),
                "model": result.get("model"),
                "trainer": TrainerSerializer(trainer, context={"request": request}).data,
            }
        )
