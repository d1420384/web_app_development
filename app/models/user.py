import sqlite3
from .db import get_db_connection

class User:
    @staticmethod
    def create(username, email, password_hash, role='user'):
        """
        新增一位使用者。
        :param username: 使用者名稱
        :param email: 電子信箱
        :param password_hash: 雜湊後的密碼
        :param role: 角色 (預設為 'user')
        :return: 成功時回傳 user_id，失敗時回傳 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)',
                (username, email, password_hash, role)
            )
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return user_id
        except sqlite3.Error as e:
            print(f"Database error in User.create: {e}")
            return None

    @staticmethod
    def get_by_id(user_id):
        """
        根據 ID 取得單一使用者。
        :param user_id: 欲查詢的 ID
        :return: 包含欄位名稱的 dict，若查無則回傳 None
        """
        try:
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
            conn.close()
            return dict(user) if user else None
        except sqlite3.Error as e:
            print(f"Database error in User.get_by_id: {e}")
            return None

    @staticmethod
    def get_by_email(email):
        """
        根據 Email 取得單一使用者。
        :param email: 欲查詢的 Email
        :return: 包含欄位名稱的 dict，若查無則回傳 None
        """
        try:
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
            conn.close()
            return dict(user) if user else None
        except sqlite3.Error as e:
            print(f"Database error in User.get_by_email: {e}")
            return None

    @staticmethod
    def get_all():
        """
        取得所有使用者。
        :return: 包含多筆使用者 dict 的 list
        """
        try:
            conn = get_db_connection()
            users = conn.execute('SELECT * FROM users').fetchall()
            conn.close()
            return [dict(u) for u in users]
        except sqlite3.Error as e:
            print(f"Database error in User.get_all: {e}")
            return []

    @staticmethod
    def update(user_id, username=None, email=None, password_hash=None, role=None):
        """
        更新使用者資料。
        :param user_id: 欲更新的 ID
        :param username: 新的使用者名稱 (若無則保持原樣)
        :param email: 新的 Email (若無則保持原樣)
        :param password_hash: 新的密碼 (若無則保持原樣)
        :param role: 新的角色 (若無則保持原樣)
        :return: 成功回傳 True，失敗或找無該使用者回傳 False
        """
        try:
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
            if not user:
                conn.close()
                return False

            new_username = username if username is not None else user['username']
            new_email = email if email is not None else user['email']
            new_password_hash = password_hash if password_hash is not None else user['password_hash']
            new_role = role if role is not None else user['role']

            conn.execute(
                'UPDATE users SET username = ?, email = ?, password_hash = ?, role = ? WHERE id = ?',
                (new_username, new_email, new_password_hash, new_role, user_id)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Database error in User.update: {e}")
            return False

    @staticmethod
    def delete(user_id):
        """
        刪除一位使用者。
        :param user_id: 欲刪除的 ID
        :return: 成功回傳 True，失敗回傳 False
        """
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Database error in User.delete: {e}")
            return False
