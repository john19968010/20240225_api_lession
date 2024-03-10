from datetime import datetime, timedelta
from typing import Any
import pymysql
from flask_jwt_extended import create_access_token

######## Response ########


def success(data: Any = "", code: int = 200) -> tuple[dict, int]:
    if not data:
        return {"message": "success"}, code
    return {
        "message": "success",
        "data": data,
        "datetime": datetime.utcnow().isoformat(),
    }, code


def failure(message: str = "failure", code: int = 500) -> tuple[dict, int]:
    return {"message": message}, code


######## DB ########


def db_init():
    db = pymysql.connect(
        host="127.0.0.1", user="root", password="root", port=8889, db="user"
    )
    cursor = db.cursor(pymysql.cursors.DictCursor)
    return db, cursor


####### jwt token ########


def generate_access_token(identity: dict[str, Any]) -> str:
    token = create_access_token(identity=identity, expires_delta=timedelta(days=1))
    return token
