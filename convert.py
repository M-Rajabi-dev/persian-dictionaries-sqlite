import os
import sys
import types
import sqlite3

if "lzo" not in sys.modules:
    try:
        import lzo
    except ImportError:
        sys.modules["lzo"] = types.ModuleType("lzo")

from readmdict import MDX

DICTIONARIES = [
    {
        "source": os.path.join("source_repo", "AmidMdx", "Amid Dictionary.mdx"),
        "fallback": "Amid Dictionary.mdx",
        "output": "amid.sqlite",
        "name": "Amid"
    },
    {
        "source": os.path.join("source_repo", "MoinMdx", "Moin Dictionary.mdx"),
        "fallback": "Moin Dictionary.mdx",
        "output": "moin.sqlite",
        "name": "Moin"
    },
    {
        "source": os.path.join("source_repo", "DehkhodaMdx", "Dehkhoda Dictionary.mdx"),
        "fallback": "Dehkhoda Dictionary.mdx",
        "output": "dehkhoda.sqlite",
        "name": "Dehkhoda"
    }
]

def convert_mdx_to_sqlite(mdx_path, db_path):
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("PRAGMA synchronous = OFF;")
    cur.execute("PRAGMA journal_mode = MEMORY;")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL,
            meaning TEXT NOT NULL
        )
    """)

    mdx = MDX(mdx_path)
    batch = []
    total = 0

    for key, val in mdx.items():
        word = key.decode("utf-8", errors="ignore").strip() if isinstance(key, bytes) else str(key).strip()
        meaning = val.decode("utf-8", errors="ignore").strip() if isinstance(val, bytes) else str(val).strip()

        if word and meaning:
            batch.append((word, meaning))
            total += 1

        if len(batch) >= 10000:
            cur.executemany("INSERT INTO words (word, meaning) VALUES (?, ?)", batch)
            conn.commit()
            batch = []

    if batch:
        cur.executemany("INSERT INTO words (word, meaning) VALUES (?, ?)", batch)
        conn.commit()

    cur.execute("CREATE INDEX IF NOT EXISTS idx_word ON words(word);")
    cur.execute("PRAGMA optimize;")
    conn.commit()
    conn.execute("VACUUM;")
    conn.close()


    return total

def main():
    for item in DICTIONARIES:
        src = item["source"]
        if not os.path.exists(src):
            src = item["fallback"]
        if not os.path.exists(src):
            print(f"Skipping {item['name']}: {src} not found")
            continue

        print(f"Converting {item['name']} from {src} to {item['output']}...")
        count = convert_mdx_to_sqlite(src, item["output"])
        print(f"Finished {item['name']}: {count} entries")

if __name__ == "__main__":
    main()
