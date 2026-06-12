import socket

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from academics.models import Unit
from attendance.models import AttendanceSession
from institutions.models import Institution
from trainers.models import Trainer


def get_lan_addresses(request):
    port = request.get_port() or "8000"
    addresses = []
    seen = set()

    def add_address(ip_address):
        if not ip_address or ip_address.startswith("127."):
            return
        if ip_address in seen:
            return
        seen.add(ip_address)
        addresses.append(
            {
                "ip": ip_address,
                "backend_url": f"http://{ip_address}:{port}",
                "health_url": f"http://{ip_address}:{port}/api/health/",
            }
        )

    hostname = socket.gethostname()
    try:
        for result in socket.getaddrinfo(hostname, None, socket.AF_INET):
            add_address(result[4][0])
    except socket.gaierror:
        pass

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(("8.8.8.8", 80))
            add_address(sock.getsockname()[0])
    except OSError:
        pass

    return {
        "hostname": hostname,
        "request_host": request.get_host(),
        "current_request_url": request.build_absolute_uri("/"),
        "addresses": addresses,
    }


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    return JsonResponse({"status": "ok", "service": "clock-in-out-backend"})


@api_view(["GET"])
@permission_classes([AllowAny])
def network_info(request):
    return JsonResponse(get_lan_addresses(request))


def monitor_dashboard(request):
    active_sessions = AttendanceSession.objects.filter(is_active=True).select_related(
        "trainer",
        "unit",
    )[:8]
    context = {
        "network": get_lan_addresses(request),
        "institution_count": Institution.objects.count(),
        "trainer_count": Trainer.objects.count(),
        "unit_count": Unit.objects.count(),
        "active_session_count": AttendanceSession.objects.filter(is_active=True).count(),
        "recent_sessions": AttendanceSession.objects.select_related("trainer", "unit")[:8],
        "active_sessions": active_sessions,
    }
    return render(request, "monitor.html", context)
