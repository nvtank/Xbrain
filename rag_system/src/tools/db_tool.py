import sqlite3

from config import SQLITE_DB_PATH

def execute_sql(
    query: str
):

    print()
    print("=" * 60)
    print("[TOOL] DATABASE QUERY")
    print(query)
    print("=" * 60)

    conn = sqlite3.connect(
        SQLITE_DB_PATH
    )

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(query)

    rows = cursor.fetchall()

    results = []

    for row in rows:

        results.append(
            dict(row)
        )

    print()
    print("[TOOL] DATABASE RESULTS")

    for row in results:
        print(row)

    print("=" * 60)
    print()

    conn.close()

    return results
