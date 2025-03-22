from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Article, Stock, Vente, VenteArticle, Utilisateur
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'une_clé_secrète'

# Initialisation de la base de données
db.init_app(app)

# Création des tables (à exécuter une seule fois)
with app.app_context():
    db.create_all()

# Routes pour les articles
@app.route('/')
def index():
    articles = Article.query.all()
    return render_template('index.html', articles=articles)

@app.route('/ajouter', methods=['GET', 'POST'])
def ajouter():
    if request.method == 'POST':
        nom = request.form['nom']
        quantite = int(request.form['quantite'])
        prix = float(request.form['prix'])
        article = Article(nom=nom, quantite=quantite, prix=prix)
        db.session.add(article)
        db.session.commit()
        flash('Article ajouté avec succès !', 'success')
        return redirect(url_for('index'))
    return render_template('ajouter.html')

@app.route('/modifier/<int:id>', methods=['GET', 'POST'])
def modifier(id):
    article = Article.query.get_or_404(id)
    if request.method == 'POST':
        article.nom = request.form['nom']
        article.quantite = int(request.form['quantite'])
        article.prix = float(request.form['prix'])
        db.session.commit()
        flash('Article modifié avec succès !', 'success')
        return redirect(url_for('index'))
    return render_template('modifier.html', article=article)

@app.route('/supprimer/<int:id>', methods=['POST'])
def supprimer(id):
    article = Article.query.get_or_404(id)
    db.session.delete(article)
    db.session.commit()
    flash('Article supprimé avec succès !', 'success')
    return redirect(url_for('index'))

# Routes pour les ventes
@app.route('/vendre', methods=['GET', 'POST'])
def vendre():
    if request.method == 'POST':
        id_article = int(request.form['id_article'])
        quantite_vendue = int(request.form['quantite_vendue'])
        article = Article.query.get_or_404(id_article)

        if article.quantite >= quantite_vendue:
            # Créer une nouvelle vente
            vente = Vente(total=quantite_vendue * article.prix)
            db.session.add(vente)
            db.session.commit()

            # Ajouter l'article vendu à la table Vente_Article
            vente_article = VenteArticle(
                id_vente=vente.id_vente,
                id_article=article.id,
                quantite_vendue=quantite_vendue,
                prix_unitaire=article.prix
            )
            db.session.add(vente_article)

            # Mettre à jour la quantité disponible
            article.quantite -= quantite_vendue
            db.session.commit()

            flash(f'{quantite_vendue} {article.nom}(s) vendu(s) avec succès !', 'success')
        else:
            flash('Stock insuffisant !', 'error')
        return redirect(url_for('index'))
    articles = Article.query.all()
    return render_template('vendre.html', articles=articles)

@app.route('/consulter')
def consulter():
    ventes = Vente.query.all()
    return render_template('consulter.html', ventes=ventes)

if __name__ == '__main__':
    app.run(debug=True)