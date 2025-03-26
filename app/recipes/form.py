from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField, FieldList, FormField
from wtforms.validators import DataRequired, NumberRange

class IngredientForm(FlaskForm):
    name = StringField('Ingrediente', validators=[DataRequired()])
    quantity = StringField('Cantidad', validators=[DataRequired()])

class RecipeForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired()])
    description = TextAreaField('Descripción', validators=[DataRequired()])
    prep_time = IntegerField('Tiempo preparación (min)', validators=[DataRequired(), NumberRange(min=1)])
    cook_time = IntegerField('Tiempo cocción (min)', validators=[NumberRange(min=0)])
    servings = IntegerField('Porciones', validators=[DataRequired(), NumberRange(min=1)])
    category = SelectField('Categoría', choices=[
        ('desayuno', 'Desayuno'),
        ('almuerzo', 'Almuerzo'),
        ('cena', 'Cena'),
        ('vegetariano', 'Vegetariano'),
        ('rapida', 'Rápida')
    ], validators=[DataRequired()])
    ingredients = FieldList(FormField(IngredientForm), min_entries=1)