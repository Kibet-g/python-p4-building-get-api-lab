from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy.orm import Session

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    with Session(db.engine) as session:
        bakeries = session.query(Bakery).all()
        return jsonify([bakery.to_dict(rules=('-baked_goods',)) for bakery in bakeries])

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    with Session(db.engine) as session:
        bakery = session.get(Bakery, id)
        if not bakery:
            return make_response({"error": "Bakery not found"}, 404)
        return jsonify(bakery.to_dict(rules=('baked_goods',)))

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    with Session(db.engine) as session:
        baked_goods = session.query(BakedGood).order_by(BakedGood.price.desc()).all()
        return jsonify([baked_good.to_dict(rules=('-bakery',)) for baked_good in baked_goods])

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    with Session(db.engine) as session:
        baked_good = session.query(BakedGood).order_by(BakedGood.price.desc()).first()
        if not baked_good:
            return make_response({"error": "No baked goods found"}, 404)
        return jsonify(baked_good.to_dict(rules=('-bakery',)))

if __name__ == '__main__':
    app.run(port=5555, debug=True)
