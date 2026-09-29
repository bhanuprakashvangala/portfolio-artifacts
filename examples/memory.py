"""Persistent note retrieval using SQLite FTS5; lexical, not embedding retrieval."""
import argparse
import json
import re
import sqlite3


class Memory:
    def __init__(self, path):
        self.db = sqlite3.connect(path)
        self.db.execute('CREATE VIRTUAL TABLE IF NOT EXISTS notes USING fts5(text)')

    def add(self, text):
        if not text.strip():
            raise ValueError('Note must not be empty')
        with self.db:
            cursor = self.db.execute('INSERT INTO notes(text) VALUES (?)', (text,))
        return cursor.lastrowid

    def search(self, query, limit=5):
        if not isinstance(limit, int) or not 1 <= limit <= 100:
            raise ValueError('Limit must be between 1 and 100')
        tokens = re.findall(r'\w+', query, flags=re.UNICODE)
        if not tokens:
            return []
        expression = ' OR '.join('"' + token + '"' for token in tokens)
        return [dict(id=row[0], text=row[1]) for row in self.db.execute(
            'SELECT rowid, text FROM notes WHERE notes MATCH ? ORDER BY rank, rowid LIMIT ?',
            (expression, limit))]

    def close(self):
        self.db.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('database')
    parser.add_argument('action', choices=['add', 'search'])
    parser.add_argument('text')
    args = parser.parse_args()
    memory = Memory(args.database)
    try:
        print(json.dumps(memory.add(args.text) if args.action == 'add' else memory.search(args.text), ensure_ascii=False))
    except (ValueError, sqlite3.Error) as exc:
        parser.exit(2, f'Error: {exc}\n')
    finally:
        memory.close()
