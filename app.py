from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from config import Config
from extensions import db

# =====================================
# CREATE FLASK APP
# =====================================

app = Flask(__name__)
print("CI/CD TEST SUCCESS")
# =====================================
# ENABLE CORS
# =====================================

CORS(
    app,
    resources={
        r"/*": {
            "origins": "*"
        }
    }
)


# =====================================
# LOAD CONFIG
# =====================================

app.config.from_object(Config)

# =====================================
# JWT SETUP
# =====================================

jwt = JWTManager(app)

# =====================================
# DATABASE INIT
# =====================================

db.init_app(app)

# =====================================
# IMPORT MODELS
# =====================================

from models.user_model import User
from models.expense_model import Expense

# =====================================
# HOME ROUTE
# =====================================

@app.route("/")
def home():

    return {
        "message": "Flask Backend Running 🚀",
        "database": "MySQL Connected",
        "status": "success"
    }

# =====================================
# IMPORT ROUTES
# =====================================

from routes.auth_routes import auth
from routes.expense_routes import expense

# =====================================
# REGISTER BLUEPRINTS
# =====================================

app.register_blueprint(auth)

app.register_blueprint(expense)

# =====================================
# CREATE DATABASE TABLES
# =====================================

with app.app_context():

    db.create_all()

# =====================================
# RUN SERVER
# =====================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )