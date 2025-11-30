from __future__ import annotations
import os
import mysql.connector
from mysql.connector import Error
import bcrypt

# A class to access the database
class Database:
    def __init__(self):
        self.config = {
            "host": os.getenv("DB_HOST", "localhost"),
            "user": os.getenv("DB_USER", "root"),
            "password": os.getenv("DB_PASSWORD", "1234"),
            "database": os.getenv("DB_DATABASE", "checkers_db"),
        }

    # Connect to the locally stored DB
    def connect(self):
        try:
            return mysql.connector.connect(**self.config)
        except mysql.connector.Error as err:
            print(f"[DB] Connection failed: {err}")
            return None


    @staticmethod
    # Helper method for encryption
    def _to_bytes(x) -> bytes:
        if isinstance(x, (bytes, bytearray)):
            return bytes(x)
        return str(x).encode("utf-8")

    @staticmethod
    # Helper method for encryption
    def _looks_like_bcrypt(h: bytes) -> bool:
        return h.startswith(b"$2a$") or h.startswith(b"$2b$") or h.startswith(b"$2y$")

    # Returns user from the database
    def get_user(self, username: str) -> dict | None:
        if not username:
            return None
        conn = self.connect()
        if conn is None:
            return None
        try:
            with conn.cursor(dictionary=True) as cursor:
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

    # Creates a new user and stores it into database
    def create_user(self, username: str, password: str) -> bool:
        salt_bytes = bcrypt.gensalt()
        hash_bytes = bcrypt.hashpw(password.encode("utf-8"), salt_bytes)
        salt_str = salt_bytes.decode("utf-8")
        hash_str = hash_bytes.decode("utf-8")

        conn = self.connect()
        if conn is None:
            print("Connection failed")
            return False
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (username, salt, hash) VALUES (%s, %s, %s)",
                    (username, salt_str, hash_str),
                )
            conn.commit()
            return True
        except Error as e:
            print("Failed to create user:", e)
            return False
        finally:
            conn.close()

    # Retrieves user and login details from database, and tests if it matches
    def correct_password(self, username: str, password: str) -> bool:
        user = self.get_user(username)
        stored_hash = user.get("hash")
        stored_hash_b = self._to_bytes(stored_hash)
        ok = bcrypt.checkpw(password.encode("utf-8"), stored_hash_b)
        return not ok

    def create_record(self, username: str, win: bool):
        if conn is None:
            print("Connection failed")
            return False
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO records (username, win) VALUES (%s, %s)",
                    (username, win)
                )
            conn.commit()
            return True
        except Error as e:
            print("Failed to create record:", e)
            return False
        finally:
            conn.close()

    def get_record(self, username: str):
        if conn is None:
            print("Connection failed")
            return False
        try:
            with conn.cursor() as cursor:
                query = """
                        SELECT 
                            ROUND(100.0 * SUM(CASE WHEN win = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) AS win_percentage
                        FROM records
                        WHERE username = %s
                        """
                cursor.execute(query, (username,))
                result = cursor.fetchone()
                if result and result[0] is not None:
                    return result[0]
                else:
                    return 0.0
        except Exception as e:
            print(f"[DB] get_record Error: {e}")
            return False
