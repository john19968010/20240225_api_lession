import os
from flask import Flask
from flask_restful import Api
from user.view import Member, SingleMember, Login
from flask_jwt_extended import JWTManager
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec


app = Flask(__name__)
api = Api(app)

app.config["DEBUG"] = True
app.config["JWT_SECRET_KEY"] = os.getenv(
    "SECRET_KEY", "SECRET_KEY"
)  # JWT token setting

# Swagger setting
app.config.update(
    {
        "APISPEC_SPEC": APISpec(
            title="Awesome Project",
            version="v1",
            plugins=[MarshmallowPlugin()],
            securityDefinitions={
                "bearer": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "Authorization",
                }
            },
            openapi_version="2.0.0",
        ),
        "APISPEC_SWAGGER_URL": "/swagger/",  # URI to access API Doc JSON
        "APISPEC_SWAGGER_UI_URL": "/swagger-ui/",  # URI to access UI of API Doc
    }
)
docs = FlaskApiSpec(app)
JWTManager(app)


api.add_resource(Member, "/members")
docs.register(Member)
api.add_resource(SingleMember, "/member/<int:id>")
docs.register(SingleMember)
api.add_resource(Login, "/login")
docs.register(Login)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10001, debug=True)
