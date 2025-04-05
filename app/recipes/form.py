from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired

class RecipeForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired()])
    category = SelectField('Categoría', choices=[
        ('breakfast', 'Desayuno'),
        ('lunch', 'Almuerzo'),
        ('dinner', 'Cena')
    ], validators=[DataRequired()])
    ingredients = TextAreaField('Ingredientes', validators=[DataRequired()])
    instructions = TextAreaField('Instrucciones', validators=[DataRequired()])
    submit = SubmitField('Guardar')