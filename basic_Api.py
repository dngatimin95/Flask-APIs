from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Boolean, nullable=False)

db.create_all() #delete after running once

user_args = reqparse.RequestParser()
user_args.add_argument("name", type=str, help="Name of user", required=True)
user_args.add_argument("age", type=int, help="Age of user")
user_args.add_argument("gender", type=bool, help="Gender of user")

user_update_args = reqparse.RequestParser()
user_update_args.add_argument("name", type=str, help="Name of user")
user_update_args.add_argument("age", type=int, help="Age of user")
user_update_args.add_argument("gender", type=bool, help="Gender of user")

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'age': fields.Integer,
    'gender': fields.Boolean
}

class Users(Resource):
    @marshal_with(resource_fields)
    def get(self, id):
        res = UserModel.query.filter_by(id=id).first()
        if not res:
            abort(404, message="Id does not exist")
        return res

    @marshal_with(resource_fields)
    def post(self, id):
        args = user_args.parse_args()
        res = UserModel.query.filter_by(id=id).first()
        if res:
            abort(409, message="Id already exists")

        user = UserModel(id=id, name=args['name'], age=args['age'], gender=args['gender'])
        db.session.add(user)
        db.session.commit()
        return user, 201

    @marshal_with(resource_fields)
    def patch(self, id):
        args = user_update_args.parse_args()
        res = UserModel.query.filter_by(id=id).first()
        if not res:
            abort(404, message="Id does not exist")

        if args['name']:
            res.name = args['name']
        if args['age']:
            res.age = args['age']
        if args['gender']:
            res.gender = args['gender']

        db.session.commit()
        return res

    @marshal_with(resource_fields)
    def delete(self, id):
        res = UserModel.query.filter_by(id=id).first()
        if not res:
            abort(404, message="Id does not exist")
        #UserModel.query.filter_by(id=id).delete()
        db.session.delete(res)
        db.session.commit()
        return '', 204

api.add_resource(Users, "/users/<int:id>")

if __name__ == "__main__":
    app.run(debug=True)
