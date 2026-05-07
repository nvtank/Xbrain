import httpx

from config import (
    MONITORING_API_URL
)

def get_services():

    print()
    print("=" * 60)
    print("[TOOL] LIST SERVICES")
    print("=" * 60)

    response = httpx.get(
        f"{MONITORING_API_URL}/services"
    )

    return response.json()

def get_service_status(
    service_name: str
):

    print()
    print("=" * 60)
    print(
        f"[TOOL] SERVICE STATUS "
        f"({service_name})"
    )
    print("=" * 60)

    response = httpx.get(
        f"{MONITORING_API_URL}/status/{service_name}"
    )

    return response.json()

def get_service_metrics(
    service_name: str
):

    print()
    print("=" * 60)
    print(
        f"[TOOL] SERVICE METRICS "
        f"({service_name})"
    )
    print("=" * 60)

    response = httpx.get(
        f"{MONITORING_API_URL}/metrics/{service_name}"
    )

    return response.json()

def get_incidents():

    print()
    print("=" * 60)
    print("[TOOL] INCIDENT HISTORY")
    print("=" * 60)

    response = httpx.get(
        f"{MONITORING_API_URL}/incidents"
    )

    return response.json()
