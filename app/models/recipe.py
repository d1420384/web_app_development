from .db import get_db_connection

class Recipe:
    @staticmethod
    def create(user_id, title, ingredients, steps, image_url=None, is_public=0):
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

    @staticmethod
    def get_by_id(recipe_id):
        conn = get_db_connection()
        recipe = conn.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,)).fetchone()
        conn.close()
        return dict(recipe) if recipe else None

    @staticmethod
    def get_all(is_public=None):
        conn = get_db_connection()
        if is_public is not None:
            recipes = conn.execute('SELECT * FROM recipes WHERE is_public = ? ORDER BY created_at DESC', (is_public,)).fetchall()
        else:
            recipes = conn.execute('SELECT * FROM recipes ORDER BY created_at DESC').fetchall()
        conn.close()
        return [dict(r) for r in recipes]

    @staticmethod
    def get_by_user_id(user_id):
        conn = get_db_connection()
        recipes = conn.execute('SELECT * FROM recipes WHERE user_id = ? ORDER BY created_at DESC', (user_id,)).fetchall()
        conn.close()
        return [dict(r) for r in recipes]

    @staticmethod
    def update(recipe_id, title=None, image_url=None, ingredients=None, steps=None, is_public=None):
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

    @staticmethod
    def delete(recipe_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
        conn.commit()
        conn.close()
        return True
