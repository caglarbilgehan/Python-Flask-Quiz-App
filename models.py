from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Soru(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    soru_metin = db.Column(db.String(255), nullable=False)
    secenek_a = db.Column(db.String(255), nullable=False)
    secenek_b = db.Column(db.String(255), nullable=False)
    secenek_c = db.Column(db.String(255), nullable=False)
    dogru_cevap = db.Column(db.String(1), nullable=False)

class KullaniciSkor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kullanici_id = db.Column(db.String(100), nullable=False)
    skor = db.Column(db.Integer, nullable=False)