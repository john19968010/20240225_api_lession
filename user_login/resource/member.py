import pymysql
from flask_restful import Resource, reqparse
from flask_apispec import MethodResource, marshal_with, doc, use_kwargs
from flask import jsonify
from flask_jwt_extended import create_access_token, jwt_required
from . import route_model
from datetime import timedelta


def db_init():
    db = pymysql.connect(
        host="127.0.0.1", user="root", password="root", port=8889, db="user"
    )
    cursor = db.cursor(pymysql.cursors.DictCursor)
    return db, cursor


def get_access_token(account):
    token = create_access_token(
        identity={"account": account}, expires_delta=timedelta(days=1)
    )
    return token


security_params = [{"bearer": []}]


class Login(MethodResource):
    @doc(description="login API", tags=["Login"])
    @use_kwargs(route_model.LoginSchema, location="form")
    @marshal_with(route_model.LoginResponse, code=200)
    def post(self, **kwargs):
        db, cursor = db_init()
        account, password = kwargs["account"], kwargs["password"]
        sql = f"SELECT * FROM user.member WHERE account = '{account}' AND password = '{password}';"
        cursor.execute(sql)
        user = cursor.fetchall()
        db.close()

        if user != ():
            token = get_access_token(account)
            data = {"message": f"Welcome back {user[0]['name']}", "token": token}
            return data, 200

        return jsonify({"message": "Account or password is wrong"})


class Member(MethodResource):
    @doc(description="Get members", tags=["User"])
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
        return {"data": users}, 200

    @doc(description="create members", tags=["User"], security=security_params)
    @use_kwargs(route_model.MemberPostSchema, location="form")
    @marshal_with(route_model.MemberPostRes, code=200)
    @jwt_required()
    def post(self, **kwargs):
        db, cursor = db_init()

        user = {
            "name": kwargs["name"],
            "gender": kwargs["gender"],
            "birth": kwargs.get("birth") or "1900-01-01",
            "note": kwargs.get("note"),
            "account": kwargs["account"],
            "password": kwargs["password"],
        }
        sql = """

        INSERT INTO `user`.`member` (`name`,`gender`,`birth`,`note`,`account`,`password`)
        VALUES ('{}','{}','{}','{}','{}','{}');

        """.format(
            user["name"],
            user["gender"],
            user["birth"],
            user["note"],
            user["account"],
            user["password"],
        )
        result = cursor.execute(sql)

        message = "success" if result == 1 else "failure"

        db.commit()
        db.close()

        return jsonify({"message": message})


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
        return {"data": users}, 200

    @doc(description="update single members", tags=["User"], security=security_params)
    @use_kwargs(route_model.SingleMemberPatchRes, location="form")
    @marshal_with(route_model.SingleMemberPatcRes, code=200)
    @jwt_required()
    def patch(self, id, **kwargs):
        db, cursor = db_init()

        user = {
            "" "name": kwargs.get("name"),
            "gender": kwargs.get("gender"),
            "birth": kwargs.get("birth"),
            "note": kwargs.get("note"),
            "account": kwargs.get("account"),
            "password": kwargs.get("password"),
        }

        query = []
        for key, value in user.items():
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
        message = "success" if result == 1 else "failure"
        db.commit()
        db.close()

        return jsonify({"message": message})

    @doc(description="Delete single members", tags=["User"], security=security_params)
    @use_kwargs(route_model.MemberGetSchema, location="query")
    @marshal_with(route_model.SingleMemberDeleteRes, code=200)
    @jwt_required()
    def delete(self, **kwargs):
        db, cursor = db_init()
        sql = f'DELETE FROM `user`.`member` WHERE id = {kwargs["id"]};'
        result = cursor.execute(sql)
        message = "success" if result == 1 else "failure"
        db.commit()
        db.close()

        return jsonify({"message": message})
