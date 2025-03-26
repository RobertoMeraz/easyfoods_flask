from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.recipes.forms import RecipeForm
from app.models import Recipe, Ingredient
from app import db
from . import recipes_bp

@recipes_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    recipes = Recipe.query.order_by(Recipe.created_at.desc()).paginate(page=page, per_page=6)
    return render_template('recipes/list.html', recipes=recipes)

@recipes_bp.route('/<int:recipe_id>')
def detail(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('recipes/detail.html', recipe=recipe)

@recipes_bp.route('/crear', methods=['GET', 'POST'])
@login_required
def create():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe = Recipe(
            title=form.title.data,
            description=form.description.data,
            prep_time=form.prep_time.data,
            cook_time=form.cook_time.data,
            servings=form.servings.data,
            category=form.category.data,
            author=current_user
        )
        
        for ingredient_data in form.ingredients.data:
            ingredient = Ingredient.query.filter_by(name=ingredient_data['name'].lower()).first()
            if not ingredient:
                ingredient = Ingredient(name=ingredient_data['name'].lower())
                db.session.add(ingredient)
            recipe.ingredients.append(ingredient)
        
        db.session.add(recipe)
        db.session.commit()
        flash('¡Receta creada exitosamente!')
        return redirect(url_for('recipes.detail', recipe_id=recipe.id))
    
    return render_template('recipes/create.html', form=form)

@recipes_bp.route('/categoria/<category>')
def category(category):
    page = request.args.get('page', 1, type=int)
    recipes = Recipe.query.filter_by(category=category).paginate(page=page, per_page=6)
    category_name = dict(RecipeForm.category.choices).get(category, category)
    return render_template('recipes/category.html', recipes=recipes, category=category_name)