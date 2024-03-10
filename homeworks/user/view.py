from flask_apispec import MethodResource, marshal_with, doc, use_kwargs
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from dotenv import load_dotenv
import os

from . import route_model
from util import success, failure, db_init, generate_access_token


load_dotenv()
security_params = [{"bearer": []}]


def permission_handler(func):
    def warp(self, *args, **kwargs):
        current_user_info = get_jwt_identity()
        current_user_info_role, current_user_info_id = (
            current_user_info["role"],
            current_user_info["id"],
        )
        method = request.method

        if current_user_info_role == "SUBAM" and method == "DELETE":
            return failure("Permission denied", 403)
        elif current_user_info_role == "NORMAL":
            if method == "POST" or method == "DELETE":
                return failure("Permission denied", 403)
            elif method == "PATCH" and kwargs.get("id") != current_user_info_id:
                return failure(
                    "Permission denied, You can only update your own profile.", 403
                )

        return func(self, *args, **kwargs)

    return warp


## Login
class Login(MethodResource):
    @doc(description="login API", tags=["Login"])
    @use_kwargs(route_model.LoginSchema, location="form")
    @marshal_with(route_model.LoginRes, code=201)
    def post(self, **kwargs):
        _, cursor = db_init()
        account, password = kwargs["account"], kwargs["password"]

        if account == os.getenv("DEFAULT_AM_ACCOUNT") and password == os.getenv(
            "DEFAULT_AM_PASSWORD"
        ):
            token = generate_access_token(
                {"id": 0, "name": os.getenv("DEFAULT_AM_ACCOUNT"), "role": "AM"}
            )
            return success({"token": token})

        sql = f"SELECT * FROM user.member WHERE account = '{account}' AND password = '{password}';"
        cursor.execute(sql)
        user = cursor.fetchall()

        if user:
            user_info = user[0]

            token = generate_access_token(
                {
                    "id": user_info["id"],
                    "name": user_info["name"],
                    "role": user_info["role"],
                }
            )
            return success({"token": token}, 201)

        return failure()


## Members


class Member(MethodResource):
    @doc(description="Get members", tags=["User"], security=security_params)
    @use_kwargs(route_model.MemberGetSchema, location="query")
    @marshal_with(route_model.MemberGetRes, code=200)
    def get(self, **kwargs):
        db, cursor = db_init()

        filter_name = kwargs.get("name")
        if filter_name is None:
            sql = "SELECT * FROM user.member;"
        else:
            sql = f"SELECT * FROM user.member WHERE name LIKE '%{filter_name}%';"

        cursor.execute(sql)
        users = cursor.fetchall()
        db.close()

        return success(users)

    @doc(description="create members", tags=["User"], security=security_params)
    @use_kwargs(route_model.MemberPostSchema, location="form")
    @marshal_with(route_model.MemberPostRes, code=200)
    @jwt_required()
    @permission_handler
    def post(self, **kwargs):
        db, cursor = db_init()
        sql = """

        INSERT INTO `user`.`member` (`name`,`gender`,`birth`,`note`,`account`,`password`,`role`)
        VALUES ('{}','{}','{}','{}','{}','{}','{}');

        """.format(
            kwargs["name"],
            kwargs["gender"],
            kwargs["birth"],
            kwargs.get("note", ""),
            kwargs["account"],
            kwargs["password"],
            kwargs["role"],
        )
        result = cursor.execute(sql)

        db.commit()
        db.close()

        if result == 0:
            return failure()

        return success()


## Member


class SingleMember(MethodResource):
    # Get single by id
    @doc(description="get single members", tags=["User"], security=security_params)
    @marshal_with(route_model.SingleMemberGetRes, code=200)
    @jwt_required()
    def get(self, id):
        db, cursor = db_init()
        sql = f"SELECT * FROM user.member WHERE id = '{id}';"
        cursor.execute(sql)
        users = cursor.fetchall()
        db.close()
        return success(users)

    @doc(description="update single members", tags=["User"], security=security_params)
    @use_kwargs(route_model.SingleMemberPatchSchema, location="form")
    @marshal_with(route_model.SingleMemberPatchRes, code=200)
    @jwt_required()
    @permission_handler
    def patch(self, id, **kwargs):
        db, cursor = db_init()
        query = []
        for key, value in kwargs.items():
            if value is not None:
                query.append(f"{key} = '{value}'")
        query = ",".join(query)
        """
        UPDATE table_name
        SET column1=value1, column2=value2, column3=value3···
        WHERE some_column=some_value;

        """
        sql = """
            UPDATE user.member
            SET {}
            WHERE id = {};
        """.format(
            query, id
        )

        result = cursor.execute(sql)
        db.commit()
        db.close()
        if result == 0:
            return failure()

        return success()

    @doc(description="Delete single members", tags=["User"], security=security_params)
    @marshal_with(route_model.SingleMemberDeleteRes, code=204)
    @jwt_required()
    @permission_handler
    def delete(self, **kwargs):
        db, cursor = db_init()
        sql = f'DELETE FROM `user`.`member` WHERE id = {kwargs["id"]};'
        cursor.execute(sql)
        db.commit()
        db.close()
        return success(code=204)
