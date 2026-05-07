from src.tools.api_tool import (
    get_services,
    get_service_status,
    get_incidents
)

print()
print("SERVICES:")
print(get_services())

print()
print("PAYMENT STATUS:")
print(
    get_service_status(
        "PaymentGW"
    )
)

print()
print("INCIDENTS:")
print(
    get_incidents()[:2]
)
