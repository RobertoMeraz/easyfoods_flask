from app import db

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    prep_time = db.Column(db.Integer)  # En minutos
    category = db.Column(db.String(20), nullable=False)
    image_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=db.func.now())
    
    def __repr__(self):
        return f'<Recipe {self.title}>'