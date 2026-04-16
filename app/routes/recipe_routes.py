from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort
from functools import wraps
from app.models.recipe import Recipe

recipe_bp = Blueprint('recipe', __name__)

# 中介函數：保護需要登入的路由
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('請先登入後再進行操作！', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@recipe_bp.route('/', methods=['GET'])
def index():
    """首頁: 顯示所有公開食譜牆。"""
    recipes = Recipe.get_all(is_public=1)
    return render_template('index.html', recipes=recipes)

@recipe_bp.route('/search', methods=['GET'])
def search():
    """搜尋: 根據 query 參數搜尋公開食譜。在記憶體中進行簡易比對過濾。"""
    query = request.args.get('q', '').strip()
    if query:
        all_public_recipes = Recipe.get_all(is_public=1)
        # 不分大小寫比對標題或食材
        recipes = [r for r in all_public_recipes if query.lower() in r['title'].lower() or query.lower() in r['ingredients'].lower()]
        return render_template('index.html', recipes=recipes, search_query=query)
    
    return redirect(url_for('recipe.index'))

@recipe_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """個人收藏夾: 需要登入，顯示個人建立的所有食譜。"""
    user_id = session.get('user_id')
    recipes = Recipe.get_by_user_id(user_id)
    return render_template('recipe/dashboard.html', recipes=recipes)

@recipe_bp.route('/recipes/create', methods=['GET', 'POST'])
@login_required
def create():
    """新增食譜: GET 顯示表單；POST 驗證並儲存至資料庫。"""
    if request.method == 'POST':
        title = request.form.get('title')
        image_url = request.form.get('image_url')
        ingredients = request.form.get('ingredients')
        steps = request.form.get('steps')
        is_public = 1 if request.form.get('is_public') else 0

        if not title or not ingredients or not steps:
            flash('標題、食材與步驟為必填欄位！', 'danger')
            return render_template('recipe/create.html', action="新增")
            
        recipe_id = Recipe.create(session['user_id'], title, ingredients, steps, image_url, is_public)
        if recipe_id:
            flash('食譜建立成功！', 'success')
            return redirect(url_for('recipe.detail', id=recipe_id))
        else:
            flash('建立過程中發生錯誤', 'danger')
            
    return render_template('recipe/create.html', action="新增")

@recipe_bp.route('/recipes/<int:id>', methods=['GET'])
def detail(id):
    """食譜詳細資訊: 公開或是自己建立的才允許檢視。"""
    recipe = Recipe.get_by_id(id)
    if not recipe:
        abort(404)
        
    # 私密食譜權限驗證
    if recipe['is_public'] == 0:
        if 'user_id' not in session or session['user_id'] != recipe['user_id']:
            flash('您沒有權限檢視此私人食譜。', 'danger')
            return redirect(url_for('recipe.index'))

    return render_template('recipe/detail.html', recipe=recipe)

@recipe_bp.route('/recipes/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    """編輯食譜: 驗證擁有權，GET 填寫舊資料表單，POST 做更新。"""
    recipe = Recipe.get_by_id(id)
    if not recipe or recipe['user_id'] != session['user_id']:
        flash('您沒有權限編輯此食譜', 'danger')
        return redirect(url_for('recipe.dashboard'))

    if request.method == 'POST':
        title = request.form.get('title')
        image_url = request.form.get('image_url')
        ingredients = request.form.get('ingredients')
        steps = request.form.get('steps')
        is_public = 1 if request.form.get('is_public') else 0

        if not title or not ingredients or not steps:
            flash('標題、食材與步驟皆為必填！', 'danger')
            return render_template('recipe/create.html', action="編輯", recipe=recipe)
            
        if Recipe.update(id, title=title, image_url=image_url, ingredients=ingredients, steps=steps, is_public=is_public):
            flash('食譜更新成功！', 'success')
            return redirect(url_for('recipe.detail', id=id))
        else:
            flash('更新食譜發生錯誤', 'danger')

    return render_template('recipe/create.html', action="編輯", recipe=recipe)

@recipe_bp.route('/recipes/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    """刪除食譜。"""
    recipe = Recipe.get_by_id(id)
    if recipe and recipe['user_id'] == session['user_id']:
        if Recipe.delete(id):
            flash('食譜刪除成功', 'success')
        else:
            flash('刪除時發生錯誤', 'danger')
    else:
        flash('無權限進行刪除', 'danger')
        
    return redirect(url_for('recipe.dashboard'))

@recipe_bp.route('/recipes/<int:id>/toggle', methods=['POST'])
@login_required
def toggle_visibility(id):
    """切換食譜的公開/私密狀態。"""
    recipe = Recipe.get_by_id(id)
    if recipe and recipe['user_id'] == session['user_id']:
        new_status = 0 if recipe['is_public'] == 1 else 1
        if Recipe.update(id, is_public=new_status):
            flash('已變更公開狀態！', 'success')
        else:
            flash('更新狀態失敗', 'danger')
    else:
        flash('無權限修改狀態', 'danger')
        
    return redirect(request.referrer or url_for('recipe.dashboard'))
