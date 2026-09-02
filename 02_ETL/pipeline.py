import subprocess
import sys
from pathlib import Path
from datetime import datetime


# ============================================================
# OASST1 MASTER DATA ENGINEERING PIPELINE
# ============================================================

BASE_DIR = Path(__file__).resolve().parent


def run_step(script_name, step_name):
    print("\n" + "=" * 70)
    print(f"{step_name}")
    print("=" * 70)

    script_path = BASE_DIR / script_name

    if not script_path.exists():
        print(f"ERROR: {script_name} not found.")
        sys.exit(1)

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(BASE_DIR.parent)
    )

    if result.returncode != 0:
        print(f"\nERROR: {script_name} failed.")
        print("Pipeline stopped.")
        sys.exit(result.returncode)

    print(f"\n{step_name} COMPLETED SUCCESSFULLY.")


def main():

    start_time = datetime.now()

    print("=" * 70)
    print("OASST1 MASTER DATA ENGINEERING PIPELINE")
    print("=" * 70)

    print("\nPipeline started...")
    print(f"Start time: {start_time}")

    # --------------------------------------------------------
    # STEP 1 — EXTRACT
    # --------------------------------------------------------
    run_step(
        "ingest.py",
        "[1/3] EXTRACT — DATA INGESTION"
    )

    # --------------------------------------------------------
    # STEP 2 — TRANSFORM
    # --------------------------------------------------------
    run_step(
        "transform.py",
        "[2/3] TRANSFORM — CLEANING & VALIDATION"
    )

    # --------------------------------------------------------
    # STEP 3 — LOAD
    # --------------------------------------------------------
    run_step(
        "load.py",
        "[3/3] LOAD — SQLITE DATABASE"
    )

    # --------------------------------------------------------
    # FINAL STATUS
    # --------------------------------------------------------

    end_time = datetime.now()
    duration = end_time - start_time

    print("\n" + "=" * 70)
    print("MASTER ETL PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 70)

    print(f"\nStart time : {start_time}")
    print(f"End time   : {end_time}")
    print(f"Duration   : {duration}")

    print("\nFINAL PIPELINE:")
    print("Raw Data")
    print("   ↓")
    print("Extract — ingest.py")
    print("   ↓")
    print("Transform — transform.py")
    print("   ↓")
    print("Validate")
    print("   ↓")
    print("Load — load.py")
    print("   ↓")
    print("SQLite Database")
    print("\nETL STATUS: PASSED")


if __name__ == "__main__":
    main()