from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(255), nullable=False)
    quantite = db.Column(db.Integer, nullable=False, default=0)
    prix = db.Column(db.Numeric(10, 2), nullable=False)

    # Relation avec la table Stock
    stock = db.relationship('Stock', backref='article', cascade='all, delete-orphan')
    # Relation avec la table Vente_Article
    ventes = db.relationship('VenteArticle', backref='article', cascade='all, delete-orphan')

class Stock(db.Model):
    id_stock = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_article = db.Column(db.Integer, db.ForeignKey('article.id', ondelete='CASCADE'), nullable=False)
    quantite_disponible = db.Column(db.Integer, nullable=False, default=0)

class Vente(db.Model):
    id_vente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_vente = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    total = db.Column(db.Numeric(10, 2), nullable=False)

    # Relation avec la table Vente_Article
    articles_vendus = db.relationship('VenteArticle', backref='vente', cascade='all, delete-orphan')

class VenteArticle(db.Model):
    id_vente = db.Column(db.Integer, db.ForeignKey('vente.id_vente', ondelete='CASCADE'), primary_key=True)
    id_article = db.Column(db.Integer, db.ForeignKey('article.id', ondelete='CASCADE'), primary_key=True)
    quantite_vendue = db.Column(db.Integer, nullable=False)
    prix_unitaire = db.Column(db.Numeric(10, 2), nullable=False)

class Utilisateur(db.Model):
    id_utilisateur = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    mot_de_passe = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('gestionnaire', 'vendeur'), nullable=False)