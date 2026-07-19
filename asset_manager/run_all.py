import subprocess
import sys
import time
import os
import signal

processes = []


def signal_handler(sig, frame):
    print("\n[System] Terminating all services...")
    for p in processes:
        try:
            p.terminate()
        except OSError:
            pass
    sys.exit(0)


def main():
    # Register Ctrl+C handler
    signal.signal(signal.SIGINT, signal_handler)

    # Get paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    django_dir = os.path.join(base_dir, "django_app")

    print("=" * 60)
    print("            Starting Asset Management Services")
    print("=" * 60)

    # 1. Start Django Admin (Port 8000)
    print("[1/3] Launching Django Admin Service on http://127.0.0.1:8000/admin ...")
    django_proc = subprocess.Popen(
        [sys.executable, "manage.py", "runserver", "127.0.0.1:8000"], cwd=django_dir
    )
    processes.append(django_proc)

    # Wait a moment for Django to boot up
    time.sleep(1.5)

    # 2. Start FastAPI (Port 8001)
    print("[2/3] Launching FastAPI Backend on http://127.0.0.1:8001 ...")
    print("      Swagger Documentation available at http://127.0.0.1:8001/docs")
    fastapi_proc = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "fastapi_app.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8001",
        ],
        cwd=base_dir,
    )
    processes.append(fastapi_proc)

    time.sleep(1.5)

    # 3. Start Flask Web Client (Port 8002)
    print("[3/3] Launching Flask Client Dashboard on http://127.0.0.1:8002 ...")
    flask_proc = subprocess.Popen([sys.executable, "flask_app/app.py"], cwd=base_dir)
    processes.append(flask_proc)

    print("\n" + "=" * 60)
    print("  All services running. Press Ctrl+C to terminate.")
    print("=" * 60)

    # Keep main thread alive
    try:
        while True:
            # Check if any process died
            for p in processes:
                if p.poll() is not None:
                    print(f"\n[Warning] Service with PID {p.pid} stopped unexpectedly.")
                    signal_handler(None, None)
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(None, None)


if __name__ == "__main__":
    main()
