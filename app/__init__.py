from flask import Flask, redirect, url_for, session

from app.routes import auth_bp, todo_bp

def create_app():
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )

    app.secret_key = "dev-secret-key"

    app.register_blueprint(auth_bp)
    app.register_blueprint(todo_bp)

    @app.route("/")
    def index():
        if session.get("member_id"):
            return redirect(url_for("todo.dashboard"))
        return redirect(url_for("auth.login"))

    return app