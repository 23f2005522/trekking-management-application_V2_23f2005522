from flask import Flask, jsonify
from config.config import Config
from flask_cors import CORS 
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sse import sse
from db.db import db 
from db.seed_data import master_seed
from extensions.cache import cache

#Routes import
from routes.health_routes import health_blueprint
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.staff_routes import staff_bp
from routes.trekker_routes import trekker_bp
from routes.notification_routes import notification_bp





app = Flask(__name__) # creating flask app instance

app.config.from_object(Config) # configuring app with config.py

db.init_app(app) # initializing db with app
 
migrate = Migrate(app, db) # initializing flask-migrate with app and db

jwt = JWTManager(app) # creating JWTManager instance and initializing it with app

jwt.init_app(app)  # then initializing JWTManager with app

cors_origins = Config.CORS_ORIGINS
if cors_origins.strip() == "*":
    cors = CORS(app, origins="*", supports_credentials=True)
else:
    cors = CORS(
        app,
        origins=[origin.strip() for origin in cors_origins.split(",") if origin.strip()],
        supports_credentials=True,
    )

app.register_blueprint(sse, url_prefix="/stream") # registering sse blueprint for streaming messages to clients

cache.init_app(app) # initializing cache with app


with app.app_context(): # creating app context to create tables and seed data
    from model.model import *
    db.create_all()
    if Config.RUN_SEED_ON_STARTUP:
        master_seed()
    



#registering blueprints for different routes
app.register_blueprint(health_blueprint)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(staff_bp)
app.register_blueprint(trekker_bp)
app.register_blueprint(notification_bp)









if(__name__ == "__main__") : # starting the flask app]
    app.run(debug=True)
