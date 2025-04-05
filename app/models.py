# app/models.py
from app import db
from datetime import datetime

# Tabla de relación muchos a muchos para ingredientes
receta_ingrediente = db.Table('receta_ingrediente',
    db.Column('receta_id', db.Integer, db.ForeignKey('receta.id'), primary_key=True),
    db.Column('ingrediente_id', db.Integer, db.ForeignKey('ingrediente.id'), primary_key=True),
    db.Column('cantidad', db.String(50)),
    db.Column('notas', db.Text)
)

# Tabla de relación muchos a muchos para etiquetas
receta_etiqueta = db.Table('receta_etiqueta',
    db.Column('receta_id', db.Integer, db.ForeignKey('receta.id'), primary_key=True),
    db.Column('etiqueta_id', db.Integer, db.ForeignKey('etiqueta.id'), primary_key=True)
)

class Receta(db.Model):
    __tablename__ = 'receta'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    tiempo_preparacion = db.Column(db.Integer)
    calorias = db.Column(db.Integer)
    imagen = db.Column(db.String(255))
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    categoria = db.relationship('Categoria', back_populates='recetas')
    ingredientes = db.relationship(
        'Ingrediente',
        secondary=receta_ingrediente,
        back_populates='recetas',
        lazy='dynamic'
    )
    etiquetas = db.relationship(
        'Etiqueta',
        secondary=receta_etiqueta,
        back_populates='recetas',
        lazy='dynamic'
    )

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'tiempo_preparacion': self.tiempo_preparacion,
            'calorias': self.calorias,
            'imagen': self.imagen,
            'categoria': self.categoria.nombre,
            'categoria_slug': self.categoria.slug,
            'ingredientes': [{
                'nombre': ri.ingrediente.nombre,
                'cantidad': ri.cantidad,
                'notas': ri.notas
            } for ri in self.ingredientes],
            'etiquetas': [e.nombre for e in self.etiquetas]
        }

    @classmethod
    def get_all_for_api(cls):
        return [receta.to_dict() for receta in cls.query.all()]

    @classmethod
    def get_by_id_for_api(cls, id):
        receta = cls.query.get(id)
        return receta.to_dict() if receta else None

    @classmethod
    def get_by_category_for_api(cls, category_slug):
        recetas = cls.query.join(Categoria).filter(Categoria.slug == category_slug).all()
        return [receta.to_dict() for receta in recetas]

    @classmethod
    def search_for_api(cls, query):
        recetas = cls.query.filter(
            (cls.titulo.ilike(f'%{query}%')) | 
            (cls.descripcion.ilike(f'%{query}%'))
        ).all()
        return [receta.to_dict() for receta in recetas]

class Categoria(db.Model):
    __tablename__ = 'categoria'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(50), nullable=False, unique=True)
    
    recetas = db.relationship('Receta', back_populates='categoria')

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'slug': self.slug
        }

    @classmethod
    def get_all_for_api(cls):
        return [categoria.to_dict() for categoria in cls.query.all()]

class Ingrediente(db.Model):
    __tablename__ = 'ingrediente'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    
    recetas = db.relationship(
        'Receta',
        secondary=receta_ingrediente,
        back_populates='ingredientes'
    )

class Etiqueta(db.Model):
    __tablename__ = 'etiqueta'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    
    recetas = db.relationship(
        'Receta',
        secondary=receta_etiqueta,
        back_populates='etiquetas'
    )