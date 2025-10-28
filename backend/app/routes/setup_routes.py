 ###  setup_routes.py - Helps to create DB as per dev
from fastapi import APIRouter, HTTPException
from app.database import save_db_config, load_db_config
from sqlalchemy import create_engine, text
import pymysql

router = APIRouter(prefix="/api/setup", tags=["Setup"])

@router.post("/database")
def setup_database(config: dict):
    try:
        if config["db_type"] == "mysql":
            conn = pymysql.connect(
                host=config["host"],
                user=config["user"],
                password=config["password"],
                port=int(config.get("port", 3306))
            )
            with conn.cursor() as cur:
                cur.execute(f"CREATE DATABASE IF NOT EXISTS {config['database']}")
            conn.close()

        save_db_config(config)
        return {"message": f"✅ Database '{config['database']}' configured successfully."}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
