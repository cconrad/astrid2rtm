# coding: utf-8
# stdlib
import hashlib
import sqlite3
# dependencies
import jsonpickle

__author__ = "Claus Conrad <webmaster@clausconrad.com>"

class Db(object):
    def __init__(self):
        self.conn = sqlite3.connect('a2r.db')
        self.crsr = self.conn.cursor()
        self.crsr.execute("""
            CREATE TABLE IF NOT EXISTS Migrated (
                Hash TEXT PRIMARY KEY
            )""")
        self.crsr.execute("""
            CREATE TABLE IF NOT EXISTS Settings (
                Key TEXT PRIMARY KEY,
                Value TEXT
            )""")
        self.crsr.execute("""
            CREATE TABLE IF NOT EXISTS ListMapping (
                Astrid TEXT PRIMARY KEY,
                RTM TEXT
            )""")
        self.conn.commit()

    def _get_hash(self, data):
        return hashlib.md5(jsonpickle.encode(data)).hexdigest()

    def get_task_migrated(self, data):
        hash = self._get_hash(data)
        self.crsr.execute("""
            SELECT
                1
            FROM
                Migrated
            WHERE
                Hash = ?
        """, (hash, ))
        return self.crsr.fetchone()

    def set_task_migrated(self, data):
        hash = self._get_hash(data)
        self.crsr.execute("""
            INSERT INTO Migrated (
                Hash
            ) VALUES (
                ?
            )""", (hash, ))
        self.conn.commit()

    def get_setting(self, key):
        self.crsr.execute("""
            SELECT
                Value
            FROM
                Settings
            WHERE
                Key = ?
            """, (key, ))
        row = self.crsr.fetchone()
        return row[0] if row else None

    def set_setting(self, key, value):
        self.crsr.execute("""
            INSERT INTO
                Settings (
                Key,
                Value
            ) VALUES (
                ?,
                ?
            )
            """, (key, value))
        self.conn.commit()

    def get_list_mappings(self):
        self.crsr.execute("""
            SELECT
                Astrid,
                RTM
            FROM
                ListMapping
            """)
        return {row[0]: row[1] for row in self.crsr.fetchall()}

    def __del__(self):
        self.conn.close()
