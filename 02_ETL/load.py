from pathlib import Path
import sqlite3
import pandas as pd


# ============================================================
# PATH CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROCESSED_FILE = (
    PROJECT_ROOT
    / "01_DATA"
    / "processed"
    / "oasst1_processed.csv"
)

DATABASE_DIR = PROJECT_ROOT / "03_DATABASE"

DATABASE_FILE = DATABASE_DIR / "oasst.db"

SCHEMA_FILE = DATABASE_DIR / "schema.sql"


# ============================================================
# LOAD PROCESSED DATA
# ============================================================

def load_processed_data():

    print("=" * 70)
    print("OASST1 SQLITE DATABASE LOAD")
    print("=" * 70)

    print("\n[1] Loading processed dataset...")

    df = pd.read_csv(PROCESSED_FILE)

    print(f"Records loaded : {len(df):,}")
    print(f"Columns        : {len(df.columns)}")

    return df


# ============================================================
# PREPARE CONVERSATIONS
# ============================================================

def create_conversations_table_data(df):

    print("\n[2] Preparing conversation-level data...")

    # Identify root messages
    roots = df[df["parent_id"].isna()].copy()

    conversations = (
        df.groupby("message_tree_id", as_index=False)
        .agg(
            conversation_created_at=("created_date", "min")
        )
    )

    # Find root message for each conversation
    root_messages = (
        roots[
            [
                "message_tree_id",
                "message_id"
            ]
        ]
        .rename(
            columns={
                "message_id": "root_message_id"
            }
        )
    )

    conversations = conversations.merge(
        root_messages,
        on="message_tree_id",
        how="left"
    )

    conversations = conversations[
        [
            "message_tree_id",
            "root_message_id",
            "conversation_created_at"
        ]
    ]

    print(
        f"Conversations prepared : "
        f"{len(conversations):,}"
    )

    return conversations


# ============================================================
# CREATE DATABASE + EXECUTE SCHEMA
# ============================================================

def create_database():

    print("\n[3] Creating SQLite database...")

    DATABASE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # Remove old database if it exists.
    # This guarantees a clean reproducible load.
    if DATABASE_FILE.exists():
        DATABASE_FILE.unlink()

    connection = sqlite3.connect(DATABASE_FILE)

    # Enable foreign key enforcement
    connection.execute("PRAGMA foreign_keys = ON;")

    # Read schema
    with open(
        SCHEMA_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        schema_sql = file.read()

    # Execute schema
    connection.executescript(schema_sql)

    print("Database created successfully.")

    return connection


# ============================================================
# INSERT DATA
# ============================================================

def insert_data(connection, df, conversations):

    print("\n[4] Loading data into SQLite...")

    # --------------------------------------------------------
    # Conversations
    # --------------------------------------------------------

    conversations.to_sql(
        "conversations",
        connection,
        if_exists="append",
        index=False
    )

    print(
        f"Conversations inserted : "
        f"{len(conversations):,}"
    )

    # --------------------------------------------------------
    # Messages
    # --------------------------------------------------------

    df.to_sql(
        "messages",
        connection,
        if_exists="append",
        index=False
    )

    print(
        f"Messages inserted      : "
        f"{len(df):,}"
    )

    connection.commit()


# ============================================================
# DATABASE VALIDATION
# ============================================================

def validate_database(connection):

    print("\n[5] Validating SQLite database...")

    # --------------------------------------------------------
    # Row counts
    # --------------------------------------------------------

    conversation_count = connection.execute(
        "SELECT COUNT(*) FROM conversations"
    ).fetchone()[0]

    message_count = connection.execute(
        "SELECT COUNT(*) FROM messages"
    ).fetchone()[0]

    print(
        f"Database conversations : "
        f"{conversation_count:,}"
    )

    print(
        f"Database messages      : "
        f"{message_count:,}"
    )

    # --------------------------------------------------------
    # Duplicate message IDs
    # --------------------------------------------------------

    duplicate_messages = connection.execute(
        """
        SELECT COUNT(*)
        FROM (
            SELECT message_id
            FROM messages
            GROUP BY message_id
            HAVING COUNT(*) > 1
        )
        """
    ).fetchone()[0]

    print(
        f"Duplicate message IDs  : "
        f"{duplicate_messages:,}"
    )

    # --------------------------------------------------------
    # Foreign-key violations
    # --------------------------------------------------------

    foreign_key_errors = connection.execute(
        "PRAGMA foreign_key_check;"
    ).fetchall()

    print(
        f"Foreign-key violations : "
        f"{len(foreign_key_errors):,}"
    )

    # --------------------------------------------------------
    # Table check
    # --------------------------------------------------------

    tables = connection.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name;
        """
    ).fetchall()

    print("\nDatabase tables:")

    for table in tables:
        print(f"  - {table[0]}")

    # --------------------------------------------------------
    # Final validation
    # --------------------------------------------------------

    if message_count != len(
        pd.read_csv(PROCESSED_FILE)
    ):
        raise ValueError(
            "Database message count does not "
            "match processed dataset."
        )

    if duplicate_messages != 0:
        raise ValueError(
            "Duplicate message IDs found."
        )

    if len(foreign_key_errors) != 0:
        raise ValueError(
            "Foreign-key violations found."
        )

    print("\nDatabase validation PASSED.")


# ============================================================
# MAIN PIPELINE
# ============================================================

def main():

    df = load_processed_data()

    conversations = create_conversations_table_data(df)

    connection = create_database()

    try:

        insert_data(
            connection,
            df,
            conversations
        )

        validate_database(connection)

    finally:

        connection.close()

    print("\n" + "=" * 70)
    print("DATABASE LOAD COMPLETED SUCCESSFULLY")
    print("=" * 70)

    print(
        f"\nSQLite database:"
        f"\n{DATABASE_FILE}"
    )


# ============================================================
# EXECUTION
# ============================================================

if __name__ == "__main__":
    main()