# En tu archivo de rutas principal (app/routes.py)
from flask import render_template, Blueprint

main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)
recipes_bp = Blueprint('recipes', __name__)

@main_bp.route('/')
def index():
    return render_template('main/index.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Lógica de autenticación
        pass
    return render_template('auth/login.html', form=form)

@recipes_bp.route('/recetas')
def list():
    recipes = get_all_recipes()  # Tu función para obtener recetas
    return render_template('recipes/list.html', recipes=recipes)

@recipes_bp.route('/recetas/desayunos')
def breakfast():
    breakfast_recipes = get_breakfast_recipes()
    return render_template('recipes/breakfast.html', breakfast_recipes=breakfast_recipes)

@recipes_bp.route('/recetas/<int:recipe_id>')
def detail(recipe_id):
    recipe = get_recipe_by_id(recipe_id)
    return render_template('recipes/detail.html', recipe=recipe)