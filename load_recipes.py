import json
from datetime import datetime
from app import create_app
from app.models import db, Recipe, Ingredient, User

def load_recipes():
    app = create_app()
    with app.app_context():
        # Crear usuario admin si no existe
        admin = User.query.filter_by(email='admin@easyfoods.com').first()
        if not admin:
            admin = User(
                username='admin', 
                email='admin@easyfoods.com',
                password=generate_password_hash('admin123')
            )
            db.session.add(admin)
            db.session.commit()

        # Mapeo de categorías
        categories_mapping = {
            'desayunos': 'desayuno',
            'almuerzos': 'almuerzo',
            'cenas': 'cena',
            'vegetarianas': 'vegetariano',
            'rapidas': 'rapida'
        }

        # Ruta base donde están los JSON
        base_path = 'app/recipes/data/'

        for filename, category in categories_mapping.items():
            try:
                with open(f'{base_path}{filename}.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"Procesando {len(data['recetas'])} recetas de {category}...")
                    
                    for recipe_data in data['recetas']:
                        # Verificar si la receta ya existe
                        existing_recipe = Recipe.query.filter_by(title=recipe_data['titulo']).first()
                        if existing_recipe:
                            continue
                        
                        # Crear nueva receta
                        recipe = Recipe(
                            title=recipe_data['titulo'],
                            description=recipe_data['descripcion'],
                            prep_time=recipe_data.get('tiempo_preparacion', 0),
                            cook_time=recipe_data.get('tiempo_coccion', 0),
                            servings=recipe_data.get('porciones', 1),
                            category=category,
                            image=recipe_data['imagen'].split('/')[-1] if 'imagen' in recipe_data else 'default.jpg',
                            user_id=admin.id,
                            created_at=datetime.utcnow()
                        )
                        
                        # Procesar ingredientes
                        for ing in recipe_data['ingredientes']:
                            ingredient = Ingredient.query.filter_by(name=ing['nombre'].lower()).first()
                            if not ingredient:
                                ingredient = Ingredient(name=ing['nombre'].lower())
                                db.session.add(ingredient)
                            
                            # Añadir relación con cantidad
                            db.session.execute(
                                recipe_ingredients.insert().values(
                                    recipe_id=recipe.id,
                                    ingredient_id=ingredient.id,
                                    quantity=ing.get('cantidad', '')
                                )
                            )
                        
                        db.session.add(recipe)
                    
                    db.session.commit()
                    print(f"{len(data['recetas']} recetas de {category} cargadas.")
            
            except FileNotFoundError:
                print(f"⚠️ Archivo {filename}.json no encontrado, omitiendo...")
            except Exception as e:
                print(f"❌ Error procesando {filename}.json: {str(e)}")
                db.session.rollback()

        print("✅ Carga de recetas completada!")

if __name__ == '__main__':
    load_recipes()