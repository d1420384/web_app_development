from .auth_routes import auth_bp
from .recipe_routes import recipe_bp

def register_routes(app):
    """
    將所有設計好的 Blueprint 註冊到 Flask 應用程式
    """
    app.register_blueprint(auth_bp)
    app.register_blueprint(recipe_bp)
