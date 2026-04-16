from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    處理會員註冊。
    GET: 渲染 auth/register.html 顯示註冊表單。
    POST: 接收表單並驗證，失敗則回傳錯誤訊息，成功則呼叫 Model 寫入資料重導向到登入頁。
    """
    pass

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    處理會員登入。
    GET: 渲染 auth/login.html 顯示登入表單。
    POST: 比對信箱與密碼，成功則記錄 session 並導向 dashboard。
    """
    pass

@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    """
    處理會員登出。
    清除 session 並重導向到首頁。
    """
    pass
