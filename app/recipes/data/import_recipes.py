import json
from app import create_app, db
from app.recipes.models import Recipe  # Asegúrate que este modelo existe
from datetime import datetime

def import_recipes():
    app = create_app()
    with app.app_context():
        # Tipos de recetas correspondientes a tus archivos JSON
        categories = ['breakfast', 'lunch', 'dinner', 'vegetarian', 'quick']
        
        for category in categories:
            with open(f'app/recipes/data/{category}.json', 'r') as f:
                recipes = json.load(f)
                
                for recipe_data in recipes:
                    # Transformación de datos para coincidir con tu modelo
                    recipe = Recipe(
                        title=recipe_data['nombre'],
                        description=recipe_data.get('descripcion', ''),
                        ingredients='\n'.join(recipe_data['ingredientes']),
                        instructions='\n'.join(recipe_data['instrucciones']),
                        prep_time=int(recipe_data['tiempo_preparacion'].split()[0]),
                        category=category,
                        image_url=f"/static/recipes/images/{recipe_data['imagen']}",
                        created_at=datetime.now()
                    )
                    db.session.add(recipe)
                
                db.session.commit()
                print(f"✅ {len(recipes)} recetas de {category} importadas")

if __name__ == '__main__':
    import_recipes()