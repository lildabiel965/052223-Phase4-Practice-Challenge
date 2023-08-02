from models import db, Episode, Guest, Appearance
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class Index(Resource):
    def get(self):
        return make_response('Code challenge', 200)

class Episodes(Resource):
    def get(self, id=None):
        if id is not None and id > 0:
            episode = Episode.query.filter(Episode.id == id).one_or_none()
            if episode is None:
                return make_response({"error": "Episode not found"}, 404)
            return make_response(episode.to_dict(), 200)
        elif id is not None and id <= 0:
            return make_response({"error": "Episode not found"}, 404)
        else:
            episodes = Episode.query.all()
            return make_response([episode.to_dict() for episode in episodes], 200)

    def delete(self, id):
        if id > 0:
            episode = Episode.query.filter(Episode.id == id).one_or_none()
            if episode is None:
                return make_response({"error": "Episode not found"}, 404)
            db.session.delete(episode)
            db.session.commit()
            return make_response('', 204)
        else:
            return make_response({"error": "Episode not found"}, 404)


class Guests(Resource):
    def get(self):
        guests = Guest.query.all()
        return make_response([guest.to_dict() for guest in guests], 200)

class Appearances(Resource):
    def post(self):
        data = request.get_json()
        try:
            appearance = Appearance(**data)
            db.session.add(appearance)
            db.session.commit()
            return make_response(appearance.to_dict(), 201)
        except ValueError:
            return make_response({"errors": ["validation errors"]}, 400)

api.add_resource(Index, '/')
api.add_resource(Episodes, '/episodes', '/episodes/<int:id>')
api.add_resource(Guests, '/guests')
api.add_resource(Appearances, '/appearances')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
