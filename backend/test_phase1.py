import requests

BASE_URL = "http://127.0.0.1:8000"


def check(name, condition):
    if condition:
        print(f"[PASS] {name}")
    else:
        print(f"[FAIL] {name}")
        raise SystemExit(1)


# ==========================================
# 1. API HEALTH
# ==========================================

response = requests.get(
    f"{BASE_URL}/nowcast?rain=0&offset=0"
)

check(
    "Nowcast endpoint responds",
    response.status_code == 200
)

data = response.json()

check(
    "Zones returned",
    len(data["zones"]) > 0
)


# ==========================================
# 2. ZONE STRUCTURE
# ==========================================

zone = next(
    z for z in data["zones"]
    if z["id"] == "kaloor"
)

required_fields = [
    "id",
    "name",
    "lat",
    "lng",
    "depthCm",
    "risk",
    "level",
    "recommendation",
    "population",
    "trend",
    "confidence",
    "alertLevel",
    "alertTriggered",
    "alertReasons",
    "recentReports",
    "blockedRoadReports",
]

for field in required_fields:

    check(
        f"Zone contains '{field}'",
        field in zone
    )


# ==========================================
# 3. RISK BOUNDARIES
# ==========================================

risk_tests = [
    (0, "safe"),
    (9.99, "safe"),
    (10, "watch"),
    (24.99, "watch"),
    (25, "high"),
    (49.99, "high"),
    (50, "severe"),
]


for depth, expected in risk_tests:

    from app.services.risk_service import risk_service

    result = risk_service.calculate(depth)

    check(
        f"Risk {depth}cm -> {expected}",
        result["level"] == expected
    )


# ==========================================
# 4. INVALID RAINFALL
# ==========================================

response = requests.get(
    f"{BASE_URL}/nowcast?rain=121&offset=0"
)

check(
    "Rainfall > 120 rejected",
    response.status_code == 400
)


response = requests.get(
    f"{BASE_URL}/nowcast?rain=-1&offset=0"
)

check(
    "Negative rainfall rejected",
    response.status_code == 400
)


# ==========================================
# 5. INVALID OFFSET
# ==========================================

response = requests.get(
    f"{BASE_URL}/nowcast?rain=50&offset=45"
)

check(
    "Invalid offset rejected",
    response.status_code == 400
)


# ==========================================
# 6. VALID FORECAST OFFSETS
# ==========================================

for offset in [0, 30, 60, 90, 120]:

    response = requests.get(
        f"{BASE_URL}/nowcast?rain=50&offset={offset}"
    )

    check(
        f"Offset {offset} accepted",
        response.status_code == 200
    )


# ==========================================
# 7. REPORT API
# ==========================================

response = requests.get(
    f"{BASE_URL}/reports"
)

check(
    "Reports endpoint responds",
    response.status_code == 200
)


reports = response.json()

check(
    "Reports are returned",
    len(reports) > 0
)


# ==========================================
# 8. RECENT REPORT API
# ==========================================

response = requests.get(
    f"{BASE_URL}/reports/recent?minutes=60"
)

check(
    "Recent reports endpoint responds",
    response.status_code == 200
)

recent = response.json()

check(
    "Recent reports response is a list",
    isinstance(recent, list)
)

check(
    "Recent reports are returned",
    len(recent) > 0
)

# ==========================================
# 9. KALOOR ALERT INTEGRATION
# ==========================================

response = requests.get(
    f"{BASE_URL}/nowcast?rain=50&offset=0"
)

data = response.json()

kaloor = next(
    z for z in data["zones"]
    if z["id"] == "kaloor"
)

check(
    "Kaloor trend detected",
    kaloor["trend"] in [
        "rising",
        "falling",
        "steady"
    ]
)

check(
    "Alert level valid",
    kaloor["alertLevel"] in [
        "safe",
        "watch",
        "high",
        "severe"
    ]
)

check(
    "Alert trigger is boolean",
    isinstance(
        kaloor["alertTriggered"],
        bool
    )
)

check(
    "Recent report count valid",
    kaloor["recentReports"] >= 0
)

check(
    "Blocked road count valid",
    kaloor["blockedRoadReports"] >= 0
)


# ==========================================
# COMPLETE
# ==========================================

print()
print("=" * 50)
print("PHASE 1 AUTOMATED VERIFICATION COMPLETE")
print("=" * 50)