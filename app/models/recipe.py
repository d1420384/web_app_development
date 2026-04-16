import sqlite3
from .db import get_db_connection

class Recipe:
    @staticmethod
    def create(user_id, title, ingredients, steps, image_url=None, is_public=0):
        """
        新增一筆食譜。
        :param user_id: 建立的會員 ID
        :param title: 食譜標題
        :param ingredients: 食材清單
        :param steps: 製作步驟
        :param image_url: 圖片網址 (可選)
        :param is_public: 是否公開 (1 為公開，0 為私密)
        :return: 成功時回傳 recipe_id，失敗時回傳 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO recipes (user_id, title, image_url, ingredients, steps, is_public)
                VALUES (?, ?, ?, ?, ?, ?)
                ''',
                (user_id, title, image_url, ingredients, steps, is_public)
            )
            conn.commit()
            recipe_id = cursor.lastrowid
            conn.close()
            return recipe_id
        except sqlite3.Error as e:
            print(f"Database error in Recipe.create: {e}")
            return None

    @staticmethod
    def get_by_id(recipe_id):
        """
        根據 ID 取得單筆食譜。
        :param recipe_id: 食譜的 ID
        :return: 包含欄位名稱的 dict，若查無則回傳 None
        """
        try:
            conn = get_db_connection()
            recipe = conn.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,)).fetchone()
            conn.close()
            return dict(recipe) if recipe else None
        except sqlite3.Error as e:
            print(f"Database error in Recipe.get_by_id: {e}")
            return None

    @staticmethod
    def get_all(is_public=None):
        """
        取得多筆食譜。
        :param is_public: 傳入 1 代表取得公開食譜，0 取私密，None 取全部
        :return: 包含多筆食譜 dict 的 list
        """
        try:
            conn = get_db_connection()
            if is_public is not None:
                recipes = conn.execute('SELECT * FROM recipes WHERE is_public = ? ORDER BY created_at DESC', (is_public,)).fetchall()
            else:
                recipes = conn.execute('SELECT * FROM recipes ORDER BY created_at DESC').fetchall()
            conn.close()
            return [dict(r) for r in recipes]
        except sqlite3.Error as e:
            print(f"Database error in Recipe.get_all: {e}")
            return []

    @staticmethod
    def get_by_user_id(user_id):
        """
        取得特定使用者的所有食譜。
        :param user_id: 欲查詢的會員 ID
        :return: 包含多筆食譜 dict 的 list
        """
        try:
            conn = get_db_connection()
            recipes = conn.execute('SELECT * FROM recipes WHERE user_id = ? ORDER BY created_at DESC', (user_id,)).fetchall()
            conn.close()
            return [dict(r) for r in recipes]
        except sqlite3.Error as e:
            print(f"Database error in Recipe.get_by_user_id: {e}")
            return []

    @staticmethod
    def update(recipe_id, title=None, image_url=None, ingredients=None, steps=None, is_public=None):
        """
        更新單筆食譜資料。
        :param recipe_id: 欲更新的食譜 ID
        :param title: 新標題 (若無則保持原樣)
        :param image_url: 新圖片 (若無則保持原樣)
        :param ingredients: 新食材清單 (若無則保持原樣)
        :param steps: 新步驟 (若無則保持原樣)
        :param is_public: 新狀態 (若無則保持原樣)
        :return: 成功回傳 True，失敗或找無該食譜回傳 False
        """
        try:
            conn = get_db_connection()
            recipe = conn.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,)).fetchone()
            if not recipe:
                conn.close()
                return False

            new_title = title if title is not None else recipe['title']
            new_image_url = image_url if image_url is not None else recipe['image_url']
            new_ingredients = ingredients if ingredients is not None else recipe['ingredients']
            new_steps = steps if steps is not None else recipe['steps']
            new_is_public = is_public if is_public is not None else recipe['is_public']

            conn.execute(
                '''
                UPDATE recipes 
                SET title = ?, image_url = ?, ingredients = ?, steps = ?, is_public = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                ''',
                (new_title, new_image_url, new_ingredients, new_steps, new_is_public, recipe_id)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Database error in Recipe.update: {e}")
            return False

    @staticmethod
    def delete(recipe_id):
        """
        刪除特定食譜。
        :param recipe_id: 欲刪除的食譜 ID
        :return: 成功回傳 True，失敗回傳 False
        """
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Database error in Recipe.delete: {e}")
            return False
