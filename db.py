from __future__ import annotations
import os
import mysql.connector
from mysql.connector import Error
import bcrypt


class Database:
    def __init__(self):
        self.config = {
            "host": os.getenv("DB_HOST", "localhost"),
            "user": os.getenv("DB_USER", "root"),
            "password": os.getenv("DB_PASSWORD", "1234"),
            "database": os.getenv("DB_DATABASE", "checkers_db"),
        }

    # ---------- connection ----------
    def connect(self):
        try:
            return mysql.connector.connect(**self.config)
        except mysql.connector.Error as err:
            print(f"[DB] Connection failed: {err}")
            return None

    # ---------- helpers ----------
    @staticmethod
    def _to_bytes(x) -> bytes:
        if isinstance(x, (bytes, bytearray)):
            return bytes(x)
        return str(x).encode("utf-8")

    @staticmethod
    def _looks_like_bcrypt(h: bytes) -> bool:
        return h.startswith(b"$2a$") or h.startswith(b"$2b$") or h.startswith(b"$2y$")

    # ---------- user ops ----------
    def get_user(self, username: str) -> dict | None:
        if not username:
            return None
        conn = self.connect()
        if conn is None:
            return None
        try:
            with conn.cursor(dictionary=True) as cursor:
                # Select salt because your schema requires it, though verification won’t use it.
                cursor.execute(
                    "SELECT username, salt, hash FROM users WHERE username = %s",
                    (username,),
                )
                row = cursor.fetchone()
                return row if row else None
        except Error as e:
            print(f"[DB] get_user Error: {e}")
            return None
        finally:
            conn.close()

    def create_user(self, username: str, password: str) -> tuple[bool, str]:
        # basic validation
        if not username or not password:
            return False, "Username or password is empty"
        if len(username) < 3:
            return False, "Username is too short"
        if len(password) < 6:
            return False, "Password is too short"

        # check duplicate
        if self.get_user(username):
            return False, "Username is already taken"

        # Generate bcrypt salt and hash.
        # bcrypt embeds the salt into the hash, but since your table has a NOT NULL salt column,
        # we also store the salt string returned by gensalt().
        salt_bytes = bcrypt.gensalt()                  # e.g. b"$2b$12$J7Pp9Qe9k2f1b0NqT0a3x."
        hash_bytes = bcrypt.hashpw(password.encode("utf-8"), salt_bytes)
        salt_str = salt_bytes.decode("utf-8")          # store as TEXT/VARCHAR
        hash_str = hash_bytes.decode("utf-8")          # store as TEXT/VARCHAR

        conn = self.connect()
        if conn is None:
            return False, "Connection failed"
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (username, salt, hash) VALUES (%s, %s, %s)",
                    (username, salt_str, hash_str),
                )
            conn.commit()
            return True, "Account created successfully"
        except Error as e:
            print(f"[DB] create_user Error: {e}")
            return False, f"[DB] create_user Error: {e}"
        finally:
            conn.close()

    def verify_login(self, username: str, password: str) -> tuple[bool, str]:
        user = self.get_user(username)
        if not user:
            return False, "Username not found"

        stored_hash = user.get("hash")
        if not stored_hash:
            return False, "Credentials corrupted"

        stored_hash_b = self._to_bytes(stored_hash)
        if not self._looks_like_bcrypt(stored_hash_b):
            return False, "Credentials corrupted. Please reset your password."

        try:
            ok = bcrypt.checkpw(password.encode("utf-8"), stored_hash_b)
        except ValueError:
            # e.g., badly formatted hash in DB
            return False, "Credentials corrupted. Please reset your password."
        return (True, "Login success") if ok else (False, "Incorrect password")
