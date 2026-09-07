# Persian Dictionaries SQLite

SQLite databases for Dehkhoda, Moin, and Amid dictionaries, converted from [sornay/Persian-Dictionaries](https://github.com/sornay/Persian-Dictionaries).

## Downloads

Download the `.sqlite` or compressed `.7z` files from [Releases](https://github.com/M-Rajabi-dev/persian-dictionaries-sqlite/releases).

## Schema

```sql
CREATE TABLE words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT NOT NULL,
    meaning TEXT NOT NULL
);

CREATE INDEX idx_word ON words(word);
```

## Dictionaries

| Dictionary | Entries | Raw Database | Compressed |
|---|---|---|---|
| Dehkhoda | 312,507 | `dehkhoda.sqlite` | `dehkhoda.sqlite.7z` |
| Moin | 36,000+ | `moin.sqlite` | `moin.sqlite.7z` |
| Amid | 32,000+ | `amid.sqlite` | `amid.sqlite.7z` |

## Build Locally

```bash
pip install readmdict python-lzo
python convert.py
```
