from random import randint, choice as rc
from faker import Faker

from app import app
from models import db, Game, Review, User

genres = [
    "Platformer", "Shooter", "Fighting", "Stealth", "Survival", "Rhythm", "Survival Horror",
    "Metroidvania", "Text-Based", "Visual Novel", "Tile-Matching", "Puzzle", "Action RPG",
    "MMORPG", "Tactical RPG", "JRPG", "Life Simulator", "Vehicle Simulator", "Tower Defense",
    "Turn-Based Strategy", "Racing", "Sports", "Party", "Trivia", "Sandbox"
]

platforms = [
    "NES", "SNES", "Nintendo 64", "GameCube", "Wii", "Wii U", "Nintendo Switch", "GameBoy",
    "GameBoy Advance", "Nintendo DS", "Nintendo 3DS", "XBox", "XBox 360", "XBox One",
    "XBox Series X/S", "PlayStation", "PlayStation 2", "PlayStation 3", "PlayStation 4",
    "PlayStation 5", "PSP", "PS Vita", "Genesis", "DreamCast", "PC",
]

fake = Faker()

with app.app_context():
    Review.query.delete()
    User.query.delete()
    Game.query.delete()

    users = [User(name=fake.name()) for _ in range(100)]
    db.session.add_all(users)

    games = [
        Game(
            title=fake.unique.sentence(nb_words=3),
            genre=rc(genres),
            platform=rc(platforms),
            price=randint(5, 60)
        ) for _ in range(100)
    ]
    db.session.add_all(games)

    reviews = [
        Review(
            score=randint(1, 10),
            comment=fake.sentence(),
            user=rc(users),
            game=rc(games)
        ) for _ in range(300)
    ]
    db.session.add_all(reviews)

    db.session.commit()
