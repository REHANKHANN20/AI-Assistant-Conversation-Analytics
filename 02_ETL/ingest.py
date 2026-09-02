from pathlib import Path
import pandas as pd


# --------------------------------------------------
# PATH CONFIGURATION
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DATA_DIR = PROJECT_ROOT / "01_DATA" / "raw"

TRAIN_FILE = RAW_DATA_DIR / "oasst1_train.csv"
VALIDATION_FILE = RAW_DATA_DIR / "oasst1_validation.csv"


# --------------------------------------------------
# DATA INGESTION
# --------------------------------------------------

def load_data():
    """Load the raw OASST1 train and validation datasets."""

    print("=" * 60)
    print("OASST1 DATA INGESTION")
    print("=" * 60)

    print("\nLoading training dataset...")
    train_df = pd.read_csv(TRAIN_FILE)

    print("Loading validation dataset...")
    validation_df = pd.read_csv(VALIDATION_FILE)

    print("\nDATA LOADED SUCCESSFULLY")
    print("-" * 60)

    print(f"Training records   : {len(train_df):,}")
    print(f"Validation records : {len(validation_df):,}")
    print(f"Training columns   : {len(train_df.columns)}")
    print(f"Validation columns : {len(validation_df.columns)}")

    print("\nColumns:")
    print(list(train_df.columns))

    return train_df, validation_df


# --------------------------------------------------
# EXECUTION
# --------------------------------------------------

if __name__ == "__main__":
    train_df, validation_df = load_data()