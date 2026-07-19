import subprocess
import sys
import time
import os
import requests


def test_fastapi_endpoints():
    print("[Test] Launching FastAPI testing instance on port 8091...")

    # Start FastAPI subprocess on port 8091
    proc = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "fastapi_app.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8091",
        ],
        cwd=os.path.dirname(os.path.abspath(__file__)),
    )

    # Wait for the service to start
    time.sleep(2)

    success = True
    try:
        # Test 1: Healthcheck and Stats
        print("[Test] 1. Requesting stats endpoint...")
        resp = requests.get("http://127.0.0.1:8091/api/stats")
        assert resp.status_code == 200
        stats = resp.json()
        print(f"       Total assets: {stats.get('total_assets')}")
        print(f"       Available assets: {stats.get('available_assets')}")
        assert stats.get("total_assets") == 4
        assert stats.get("available_assets") == 2
        print("       [OK] Stats endpoint verified.")

        # Test 2: Categories
        print("[Test] 2. Requesting categories endpoint...")
        resp = requests.get("http://127.0.0.1:8091/api/categories")
        assert resp.status_code == 200
        categories = resp.json()
        assert len(categories) == 4
        print(f"       Categories found: {[c['name'] for c in categories]}")
        print("       [OK] Categories endpoint verified.")

        # Test 3: Assets List
        print("[Test] 3. Requesting assets endpoint...")
        resp = requests.get("http://127.0.0.1:8091/api/assets")
        assert resp.status_code == 200
        assets = resp.json()
        assert len(assets) == 4
        print(f"       Asset names: {[a['name'] for a in assets]}")
        print("       [OK] Assets list verified.")

    except AssertionError as e:
        print(f"[ERROR] Test assertions failed! {e}")
        success = False
    except Exception as e:
        print(f"[ERROR] Test encountered exception! {e}")
        success = False
    finally:
        print("[Test] Terminating FastAPI instance...")
        proc.terminate()
        proc.wait()

    if success:
        print("[Test] INTEGRATION TESTS COMPLETED SUCCESSFULLY!")
        return 0
    else:
        print("[Test] INTEGRATION TESTS FAILED!")
        return 1


if __name__ == "__main__":
    sys.exit(test_fastapi_endpoints())
