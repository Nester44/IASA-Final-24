from flask_restful import Resource


class HelloWorld(Resource):
    def get(self):
        return {"hello": "world"}


def initialize_routes(api):
    api.add_resource(HelloWorld, "/")
