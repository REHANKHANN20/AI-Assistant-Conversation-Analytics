from pathlib import Path
import sqlite3
import pandas as pd


# ============================================================
# PATH CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATABASE_FILE = (
    PROJECT_ROOT
    / "03_DATABASE"
    / "oasst.db"
)

QUERY_FILE = Path(__file__).resolve().parent / "analysis_queries.sql"


# ============================================================
# READ SQL FILE
# ============================================================

def read_queries():

    with open(
        QUERY_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        content = file.read()

    statements = []
    current_statement = []

    for line in content.splitlines():

        current_statement.append(line)

        if sqlite3.complete_statement(
            "\n".join(current_statement)
        ):
            statement = "\n".join(
                current_statement
            ).strip()

            if statement:
                statements.append(statement)

            current_statement = []

    return statements


# ============================================================
# EXECUTE SQL ANALYSIS
# ============================================================

def main():

    print("=" * 75)
    print("OASST1 SQL ANALYSIS EXECUTION")
    print("=" * 75)

    print(f"\nDatabase:")
    print(DATABASE_FILE)

    print(f"\nQuery file:")
    print(QUERY_FILE)

    connection = sqlite3.connect(
        DATABASE_FILE
    )

    queries = read_queries()

    print(
        f"\nTotal SQL statements found : "
        f"{len(queries)}"
    )

    print("\n" + "=" * 75)

    for number, query in enumerate(
        queries,
        start=1
    ):

        print(
            f"\nQUERY {number}"
        )

        print("-" * 75)

        try:

            result = pd.read_sql_query(
                query,
                connection
            )

            if result.empty:

                print("No rows returned.")

            else:

                print(
                    result.to_string(
                        index=False
                    )
                )

        except Exception as error:

            print(
                f"ERROR in Query {number}:"
            )

            print(error)

            connection.close()

            raise

    connection.close()

    print("\n" + "=" * 75)
    print("SQL ANALYSIS COMPLETED SUCCESSFULLY")
    print("=" * 75)


if __name__ == "__main__":
    main()