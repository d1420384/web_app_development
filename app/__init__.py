from flask import Flask
from .routes import register_routes
import os

def create_app():
    app = Flask(__name__)
    
    # 基本設定，會優先取環境變數的 SECRET_KEY，如果沒有則使用預設字串
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key_default')
    
    # 註冊路由 Blueprints
    register_routes(app)
    
    return app
