from marshmallow import Schema, fields, ValidationError, validate

from util import db_init

## CommonResponse


class CommonResponse(Schema):
    message = fields.Str(example="string")


class CommonWithDataResponse(Schema):
    message = fields.Str(example="string")
    datetime = fields.Str(example="2021-10-10T10:10:10.000000")
    data = fields.Raw()


## Login
class LoginSchema(Schema):
    account = fields.Str(doc="account", example="string", required=True)
    password = fields.Str(doc="password", example="string", required=True)


class LoginRes(CommonWithDataResponse):
    data = fields.Dict()


## Member
"""
NOTE: https://marshmallow.readthedocs.io/en/stable/quickstart.html#validation-without-deserialization
Check the link above to see how to use validate.
"""


def account_exist_validator(acc: str):
    _, cursor = db_init()
    sql = f"SELECT * FROM user.member WHERE account = '{acc}'"
    cursor.execute(sql)
    user = cursor.fetchall()
    if user:
        raise ValidationError("Account already exists.")


class MemberGetSchema(Schema):
    name = fields.Str(doc="name", example="john")


class MemberGetResData(Schema):
    """
    Because we do not want to display password.
    """

    id = fields.Int()
    name = fields.Str()
    account = fields.Str()
    birth = fields.Str()
    gender = fields.Str()
    note = fields.Str()
    role = fields.Str()


class MemberGetRes(CommonWithDataResponse):
    data = fields.List(fields.Nested(MemberGetResData))


class MemberPostSchema(Schema):
    name = fields.Str(doc="names", example="string", required=True)
    gender = fields.Str(example="string", required=True)
    birth = fields.Str(example="string", required=True)
    account = fields.Str(
        example="string", required=True, validate=account_exist_validator
    )
    password = fields.Str(example="string", required=True)
    role = fields.Str(
        example="AM", required=True, validate=validate.OneOf(["AM", "SUBAM", "NORMAL"])
    )
    note = fields.Str(example="string")


class MemberPostRes(Schema):
    message = fields.Str(example="string")


## Single Member
class SingleMemberGetRes(CommonWithDataResponse):
    data = fields.List(fields.Nested(MemberGetResData))


class SingleMemberPatchSchema(Schema):
    name = fields.Str(example="string")
    gender = fields.Str(example="string")
    birth = fields.Str(example="string")
    note = fields.Str(example="string")
    password = fields.Str(example="string")
    role = fields.Str(example="AM", validate=validate.OneOf(["AM", "SUBAM", "NORMAL"]))


class SingleMemberPatchRes(CommonResponse):
    pass


class SingleMemberDeleteRes(CommonResponse):
    pass
