from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError

from models import db, User, Review, Game

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return {"message": "Welcome to the Game API!"}, 200

@app.route('/games', methods=['GET', 'POST'])
def games():
    if request.method == 'GET':
        games = [game.to_dict() for game in Game.query.all()]
        return jsonify(games), 200

    elif request.method == 'POST':
        data = request.get_json()
        try:
            new_game = Game(
                title=data['title'],
                genre=data['genre'],
                platform=data['platform'],
                price=data['price']
            )
            db.session.add(new_game)
            db.session.commit()
            return new_game.to_dict(), 201
        except IntegrityError:
            db.session.rollback()
            return {"error": "Game with the same title already exists."}, 400

@app.route('/games/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def game_by_id(id):
    game = Game.query.get_or_404(id)

    if request.method == 'GET':
        return game.to_dict(), 200

    elif request.method == 'PATCH':
        data = request.get_json()
        for key, value in data.items():
            setattr(game, key, value)
        db.session.commit()
        return game.to_dict(), 200

    elif request.method == 'DELETE':
        db.session.delete(game)
        db.session.commit()
        return {"message": "Game deleted successfully."}, 200

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    if request.method == 'GET':
        reviews = [review.to_dict() for review in Review.query.all()]
        return jsonify(reviews), 200

    elif request.method == 'POST':
        data = request.get_json()
        try:
            new_review = Review(
                score=data['score'],
                comment=data['comment'],
                game_id=data['game_id'],
                user_id=data['user_id']
            )
            db.session.add(new_review)
            db.session.commit()
            return new_review.to_dict(), 201
        except IntegrityError:
            db.session.rollback()
            return {"error": "Invalid data or duplicate review."}, 400

@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        users = [user.to_dict() for user in User.query.all()]
        return jsonify(users), 200

    elif request.method == 'POST':
        data = request.get_json()
        try:
            new_user = User(name=data['name'])
            db.session.add(new_user)
            db.session.commit()
            return new_user.to_dict(), 201
        except IntegrityError:
            db.session.rollback()
            return {"error": "User with the same name already exists."}, 400

if __name__ == '__main__':
    app.run(port=5555, debug=True)