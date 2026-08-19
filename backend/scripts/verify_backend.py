import sys
import time

import requests


BASE_URL = "http://127.0.0.1:8000"


def check(name, method="GET", path="/", expected_status=200, **kwargs):
    try:
        start = time.perf_counter()

        response = requests.request(
            method,
            f"{BASE_URL}{path}",
            timeout=15,
            **kwargs,
        )

        elapsed = (time.perf_counter() - start) * 1000

        if response.status_code != expected_status:
            print(f"❌ {name}: HTTP {response.status_code}")
            print(response.text[:500])
            return False

        print(f"✅ {name}: {elapsed:.0f} ms")
        return response.json()

    except Exception as exc:
        print(f"❌ {name}: {exc}")
        return False


def main():
    print()
    print("=" * 55)
    print("       JALNETRA BACKEND VERIFICATION")
    print("=" * 55)

    # --------------------------------------------------
    # HEALTH
    # --------------------------------------------------

    health = check("Health", path="/health")

    if not health:
        print("\n❌ Backend verification stopped.")
        sys.exit(1)

    if health.get("status") != "healthy":
        print("\n❌ Health endpoint is not healthy.")
        sys.exit(1)

    # --------------------------------------------------
    # NOWCAST
    # --------------------------------------------------

    offsets = [0, 30, 60, 90, 120]
    predictions = {}

    for offset in offsets:
        result = check(
            f"Nowcast {offset:>3} min",
            path="/nowcast",
            params={
                "rain": 50,
                "offset": offset,
            },
        )

        if not result:
            sys.exit(1)

        predictions[offset] = result

    # --------------------------------------------------
    # OFFSET VALIDATION
    # --------------------------------------------------

    print("\n" + "-" * 55)
    print("OFFSET VALIDATION")
    print("-" * 55)

    kaloor_depths = []

    for offset in offsets:
        zones = predictions[offset].get("zones", [])

        kaloor = next(
            (
                zone
                for zone in zones
                if zone.get("id") == "kaloor"
            ),
            None,
        )

        if kaloor is None:
            print(f"❌ Kaloor missing at {offset} min")
            sys.exit(1)

        depth = float(kaloor["depthCm"])
        kaloor_depths.append(depth)

        print(
            f"{offset:>3} min → "
            f"Kaloor: {depth:.2f} cm"
        )

    if len(set(kaloor_depths)) == 1:
        print("\n❌ Offset has NO effect on prediction.")
        sys.exit(1)

    print("\n✅ Offset changes prediction.")

    # --------------------------------------------------
    # ZONE VALIDATION
    # --------------------------------------------------

    print("\n" + "-" * 55)
    print("ZONE VALIDATION")
    print("-" * 55)

    zones = predictions[0].get("zones", [])

    if len(zones) < 3:
        print("❌ Fewer than 3 zones returned.")
        sys.exit(1)

    depths = []

    for zone in zones:
        depth = float(zone["depthCm"])
        risk = float(zone["risk"])

        if depth < 0:
            print(
                f"❌ Negative depth: "
                f"{zone['name']}"
            )
            sys.exit(1)

        if not 0 <= risk <= 1:
            print(
                f"❌ Invalid risk for "
                f"{zone['name']}: {risk}"
            )
            sys.exit(1)

        depths.append(depth)

        print(
            f"{zone['name']:<20} "
            f"{depth:>7.2f} cm | "
            f"risk={risk:.3f} | "
            f"{zone['level']}"
        )

    # --------------------------------------------------
    # SPATIAL VARIATION
    # --------------------------------------------------

    depth_range = max(depths) - min(depths)

    print(f"\nZones returned: {len(zones)}")
    print(
        f"Minimum depth: "
        f"{min(depths):.2f} cm"
    )
    print(
        f"Maximum depth: "
        f"{max(depths):.2f} cm"
    )
    print(
        f"Spatial depth range: "
        f"{depth_range:.2f} cm"
    )

    if depth_range < 0.10:
        print(
            "\n⚠️ WARNING: Predictions are "
            "nearly identical across zones."
        )
    else:
        print("\n✅ Spatial variation detected.")

    # --------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------

    print("\n" + "-" * 55)
    print("RESULT")
    print("-" * 55)
    print("✅ JalNetra backend verification PASSED")
    print("=" * 55)


if __name__ == "__main__":
    main()