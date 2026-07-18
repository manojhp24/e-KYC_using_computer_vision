from flask import Flask
from routes import  home_bp, verification_bp

def create_app():
    app = Flask(__name__)

    app.register_blueprint(home_bp)
    app.register_blueprint(verification_bp)

    return app

app = create_app()




if __name__ == "__main__":
    app.run(debug=True)