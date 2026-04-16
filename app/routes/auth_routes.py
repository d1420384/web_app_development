from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """處理會員註冊。"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not username or not email or not password:
            flash('所有欄位都是必填的！', 'danger')
            return render_template('auth/register.html')
            
        if password != confirm_password:
            flash('兩次輸入的密碼不一致！', 'danger')
            return render_template('auth/register.html')

        if User.get_by_email(email):
            flash('此 Email 已經被註冊過了！', 'danger')
            return render_template('auth/register.html')

        password_hash = generate_password_hash(password)
        user_id = User.create(username, email, password_hash)
        
        if user_id:
            flash('註冊成功！請登入。', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('註冊過程中發生錯誤，請稍後再試。', 'danger')
            
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """處理會員登入。"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('請輸入 Email 與密碼！', 'danger')
            return render_template('auth/login.html')

        user = User.get_by_email(email)
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash(f'歡迎回來，{user["username"]}！', 'success')
            return redirect(url_for('recipe.dashboard'))
        else:
            flash('帳號或密碼錯誤！', 'danger')
            
    return render_template('auth/login.html')

@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    """處理會員登出。"""
    session.clear()
    flash('您已成功登出。', 'info')
    return redirect(url_for('recipe.index'))
