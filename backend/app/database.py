# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import json, os
from app import db_info  # fallback dev config
from urllib.parse import quote_plus


Base = declarative_base()
engine = None
SessionLocal = None

def load_db_config():
    config_path = "config/db_config.json"
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return json.load(f)
    return None

def save_db_config(config):
    os.makedirs("config", exist_ok=True)
    with open("config/db_config.json", "w") as f:
        json.dump(config, f, indent=4)

def init_engine():
    global engine, SessionLocal
    config = load_db_config()
    if not config:
        config = db_info.db_config
        save_db_config(config)

    if config["db_type"] == "mysql":
        # 🔹 URL-encode password
        password = quote_plus(config['password'])
        url = f"mysql+pymysql://{config['user']}:{password}@{config['host']}:{config['port']}/{config['database']}"
    else:
        url = "sqlite:///./projectmaker.db"

    engine = create_engine(url, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine


# Dependency
def get_db():
    if SessionLocal is None:
        # 🔹 Make sure the engine is initialized before usage
        init_engine()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
