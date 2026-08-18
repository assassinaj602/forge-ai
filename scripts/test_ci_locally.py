"""
Local CI Pipeline Tester Script for ForgeAI.
Simulates GitHub Actions CI pipeline locally on Windows/Linux.
"""
import os
import sys
import subprocess

def run_step(title, command, cwd=None):
    print(f"\n=======================================================")
    print(f" CI Step: {title}")
    print(f"=======================================================")
    res = subprocess.run(command, shell=True, cwd=cwd)
    if res.returncode != 0:
        print(f"[FAILED] CI Step Failed with exit code {res.returncode}: {title}")
        sys.exit(res.returncode)
    print(f"[PASSED] CI Step Passed: {title}")

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    backend_dir = os.path.join(base_dir, "backend")

    os.environ["ENVIRONMENT"] = "testing"
    os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./local_ci_test.db"

    # Step 1: Alembic DB Migration Check
    run_step(
        "Alembic Database Migration Dry-Run",
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        cwd=backend_dir
    )

    # Step 2: Pytest Suite Execution
    run_step(
        "Backend Pytest Suite Execution",
        [sys.executable, "-m", "pytest", "-v"],
        cwd=backend_dir
    )

    print("\nLocal CI Simulation Completed Successfully! All checks passed.")

if __name__ == "__main__":
    main()
