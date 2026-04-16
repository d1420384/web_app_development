from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort
from app.models.recipe import Recipe

recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/', methods=['GET'])
def index():
    """
    首頁: 顯示公開食譜牆。
    """
    pass

@recipe_bp.route('/search', methods=['GET'])
def search():
    """
    搜尋: 根據 query 參數搜尋公開食譜。
    """
    pass

@recipe_bp.route('/dashboard', methods=['GET'])
def dashboard():
    """
    個人收藏夾: 需要登入，顯示個人建立的所有食譜。
    """
    pass

@recipe_bp.route('/recipes/create', methods=['GET', 'POST'])
def create():
    """
    新增食譜:
    GET 顯示表單；POST 將資料存進資料庫。
    """
    pass

@recipe_bp.route('/recipes/<int:id>', methods=['GET'])
def detail(id):
    """
    食譜詳細資訊頁面:
    公開或是自己建立的才能檢視。
    """
    pass

@recipe_bp.route('/recipes/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    """
    編輯食譜:
    驗證是否為自己的食譜，若是則允許編輯。 GET 預填表單，POST 做更新。
    """
    pass

@recipe_bp.route('/recipes/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    刪除食譜。
    """
    pass

@recipe_bp.route('/recipes/<int:id>/toggle', methods=['POST'])
def toggle_visibility(id):
    """
    切換食譜可見度 (is_public)。
    """
    pass
