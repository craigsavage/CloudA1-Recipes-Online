from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
db = SQLAlchemy(app)

#Model of the database structure
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    like = db.Column(db.Integer, default=0)
    dislike = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Recipe %r>' % self.id

# Route for adding to database
@app.route('/', methods=['POST', 'GET'])
def index():
    # Create a new recipe in database with values from the form
    if request.method == 'POST':
        recipe_title = request.form['title']
        recipe_description = request.form['description']

        if recipe_title == "" or recipe_description =="":
            return redirect('/')

        new_recipe = Recipe(title = recipe_title, description = recipe_description)

        try:
            db.session.add(new_recipe)
            db.session.commit()
            return redirect('/')
        except:
            return 'An issue occurred while adding your recipe'
    else:
        # Returns all database content
        recipes = Recipe.query.order_by(Recipe.date_created).all()
        return render_template('index.html', recipes = recipes)

# Route for deleting from the database
@app.route('/delete/<int:id>')
def delete(id):
    # Search database for that recipe then delete it
    recipe = Recipe.query.get_or_404(id)
    try:
        db.session.delete(recipe)
        db.session.commit()
        return redirect('/')
    except:
        return 'An issue occurred while deleting the recipe'

# Route for liking a recipe in the database
@app.route('/like/<int:id>', methods=['POST', 'GET'])
def like(id):
    recipe = Recipe.query.get_or_404(id)
    recipe.like = recipe.like + 1

    try:
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem liking this recipe'

# Route for disliking a recipe in the database
@app.route('/dislike/<int:id>', methods=['POST', 'GET'])
def dislike(id):
    recipe = Recipe.query.get_or_404(id)
    recipe.dislike = recipe.dislike + 1
    
    try:
        db.session.commit()
        return redirect('/')
    except:
        return'There was a problem disliking this recipe'

# Route for disliking a recipe in the database
@app.route('/search/<searchval>', methods=['POST', 'GET'])
def search(searchval):
    print(searchval, file=sys.stdout)
    # Searches is titles in database contains the searched word
    recipes = Recipe.query.filter(Recipe.title.ilike("%" + searchval + "%")).all()
    return render_template('index.html', recipes = recipes)

# Runs everything
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)