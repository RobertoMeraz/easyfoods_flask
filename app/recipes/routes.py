from app.recipes.forms import RecipeForm
from app import db
from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.recipes.forms import RecipeForm
from app.models import Recipe
from . import recipes_bp

@recipes_bp.route('/breakfast')
def breakfast():
    recipes = Recipe.query.filter_by(category='breakfast').all()
    return render_template('recipes/breakfast.html', recipes=recipes)

@recipes_bp.route('/add-recipe', methods=['GET', 'POST'])
@login_required
def add_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe = Recipe(
            title=form.title.data,
            category=form.category.data,
            ingredients=form.ingredients.data,
            instructions=form.instructions.data,
            user_id=current_user.id
        )
        db.session.add(recipe)
        db.session.commit()
        flash('¡Receta agregada!', 'success')
        return redirect(url_for('recipes.list'))
    return render_template('recipes/add.html', form=form)