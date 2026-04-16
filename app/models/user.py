from .db import get_db_connection

class User:
    @staticmethod
    def create(username, email, password_hash, role='user'):
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

    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        return dict(user) if user else None

    @staticmethod
    def get_by_email(email):
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        return dict(user) if user else None

    @staticmethod
    def get_all():
        conn = get_db_connection()
        users = conn.execute('SELECT * FROM users').fetchall()
        conn.close()
        return [dict(u) for u in users]

    @staticmethod
    def update(user_id, username=None, email=None, password_hash=None, role=None):
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

    @staticmethod
    def delete(user_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
        return True
