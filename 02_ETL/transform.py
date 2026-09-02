from pathlib import Path
import pandas as pd


# ============================================================
# PATH CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DATA_DIR = PROJECT_ROOT / "01_DATA" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "01_DATA" / "processed"

TRAIN_FILE = RAW_DATA_DIR / "oasst1_train.csv"
VALIDATION_FILE = RAW_DATA_DIR / "oasst1_validation.csv"

OUTPUT_FILE = PROCESSED_DATA_DIR / "oasst1_processed.csv"


# ============================================================
# LOAD RAW DATA
# ============================================================

def load_raw_data():

    print("=" * 70)
    print("OASST1 DATA TRANSFORMATION PIPELINE")
    print("=" * 70)

    print("\n[1] Loading raw datasets...")

    train_df = pd.read_csv(TRAIN_FILE)
    validation_df = pd.read_csv(VALIDATION_FILE)

    # Preserve the original dataset split for traceability
    train_df["source_split"] = "train"
    validation_df["source_split"] = "validation"

    print(f"Training records   : {len(train_df):,}")
    print(f"Validation records : {len(validation_df):,}")

    return train_df, validation_df


# ============================================================
# COMBINE DATA
# ============================================================

def combine_data(train_df, validation_df):

    print("\n[2] Combining train and validation data...")

    combined_df = pd.concat(
        [train_df, validation_df],
        ignore_index=True
    )

    print(f"Combined records   : {len(combined_df):,}")
    print(f"Columns            : {len(combined_df.columns)}")

    return combined_df


# ============================================================
# STANDARDIZE DATA
# ============================================================

def standardize_data(df):

    print("\n[3] Standardizing data...")

    # --------------------------------------------------------
    # Column names
    # --------------------------------------------------------

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )

    # --------------------------------------------------------
    # String fields
    # --------------------------------------------------------

    string_columns = [
        "message_id",
        "parent_id",
        "user_id",
        "text",
        "role",
        "lang",
        "review_result",
        "model_name",
        "message_tree_id",
        "tree_state",
        "emojis",
        "labels",
        "source_split"
    ]

    for column in string_columns:
        if column in df.columns:
            df[column] = df[column].astype("string")

    # Remove unnecessary leading/trailing spaces from text
    df["text"] = df["text"].str.strip()

    # --------------------------------------------------------
    # Numeric fields
    # --------------------------------------------------------

    df["review_count"] = pd.to_numeric(
        df["review_count"],
        errors="coerce"
    )

    df["rank"] = pd.to_numeric(
        df["rank"],
        errors="coerce"
    )

    # --------------------------------------------------------
    # Date/time
    # --------------------------------------------------------

    df["created_date"] = pd.to_datetime(
        df["created_date"],
        errors="coerce",
        utc=True
    )

    # --------------------------------------------------------
    # Boolean fields
    # --------------------------------------------------------

    for column in ["deleted", "synthetic"]:
        df[column] = df[column].astype("boolean")

    # review_result contains True / False / missing
    df["review_result"] = (
        df["review_result"]
        .map({
            "True": True,
            "False": False
        })
        .astype("boolean")
    )

    return df


# ============================================================
# DATA QUALITY VALIDATION
# ============================================================

def validate_data(df):

    print("\n[4] Running data quality validation...")

    # --------------------------------------------------------
    # Missing values
    # --------------------------------------------------------

    print("\nMissing values:")
    missing = df.isna().sum()

    for column, count in missing.items():
        if count > 0:
            percentage = (count / len(df)) * 100
            print(
                f"  {column:<20} "
                f"{count:>8,} "
                f"({percentage:.2f}%)"
            )

    # --------------------------------------------------------
    # Duplicate message IDs
    # --------------------------------------------------------

    duplicate_ids = df["message_id"].duplicated().sum()

    print(f"\nDuplicate message IDs : {duplicate_ids:,}")

    if duplicate_ids > 0:
        raise ValueError(
            "Duplicate message_id values detected."
        )

    # --------------------------------------------------------
    # Missing critical IDs
    # --------------------------------------------------------

    missing_message_ids = df["message_id"].isna().sum()

    print(f"Missing message IDs   : {missing_message_ids:,}")

    if missing_message_ids > 0:
        raise ValueError(
            "Critical field message_id contains missing values."
        )

    # --------------------------------------------------------
    # Empty text
    # --------------------------------------------------------

    empty_text = (
        df["text"]
        .fillna("")
        .str.strip()
        .eq("")
        .sum()
    )

    print(f"Empty text records    : {empty_text:,}")

    # --------------------------------------------------------
    # Parent relationship validation
    # --------------------------------------------------------

    all_message_ids = set(
        df["message_id"].dropna()
    )

    parent_ids = set(
        df["parent_id"].dropna()
    )

    orphan_parents = parent_ids - all_message_ids

    print(
        f"Orphan parent IDs    : "
        f"{len(orphan_parents):,}"
    )

    # --------------------------------------------------------
    # Basic range validation
    # --------------------------------------------------------

    invalid_review_count = (
        df["review_count"] < 0
    ).sum()

    print(
        f"Negative review counts: "
        f"{invalid_review_count:,}"
    )

    if invalid_review_count > 0:
        raise ValueError(
            "Negative review_count values detected."
        )

    print("\nValidation completed successfully.")


# ============================================================
# REMOVE UNUSABLE SOURCE FIELD
# ============================================================

def remove_unusable_fields(df):

    print("\n[5] Removing fields with no usable information...")

    # model_name is completely NULL in our downloaded dataset.
    if "model_name" in df.columns:

        missing_percentage = (
            df["model_name"].isna().mean() * 100
        )

        if missing_percentage == 100:
            df = df.drop(columns=["model_name"])
            print(
                "Removed 'model_name' "
                "(100% missing in source data)."
            )

    return df


# ============================================================
# SAVE PROCESSED DATA
# ============================================================

def save_processed_data(df):

    print("\n[6] Saving processed dataset...")

    PROCESSED_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # Convert timezone-aware datetime back to ISO format
    df["created_date"] = (
        df["created_date"]
        .dt.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(f"\nProcessed file created:")
    print(OUTPUT_FILE)

    print(f"\nFinal records : {len(df):,}")
    print(f"Final columns : {len(df.columns)}")


# ============================================================
# MAIN TRANSFORMATION PIPELINE
# ============================================================

def main():

    # 1. Load
    train_df, validation_df = load_raw_data()

    # 2. Combine
    df = combine_data(
        train_df,
        validation_df
    )

    # 3. Standardize
    df = standardize_data(df)

    # 4. Validate
    validate_data(df)

    # 5. Remove unusable fields
    df = remove_unusable_fields(df)

    # 6. Save
    save_processed_data(df)

    print("\n" + "=" * 70)
    print("TRANSFORMATION COMPLETED SUCCESSFULLY")
    print("=" * 70)


# ============================================================
# EXECUTION
# ============================================================

if __name__ == "__main__":
    main()