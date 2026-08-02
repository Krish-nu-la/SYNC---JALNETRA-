from app.services.zone_service import ZoneService

service = ZoneService()

zones = service.get_all_zones()

print(f"Loaded {len(zones)} zones\n")

for zone in zones:
    print(zone["name"], zone["susceptibility"])