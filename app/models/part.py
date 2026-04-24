from app.extensions import db

class PartCategory(db.Model):
    __tablename__ = 'part_categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    parts = db.relationship('Part', back_populates='category')

class Part(db.Model):
    __tablename__ = 'parts'
    id = db.Column(db.Integer, primary_key=True)
    part_number = db.Column(db.String(64), nullable=False)
    part_name = db.Column(db.String(128), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('part_categories.id'), nullable=False)
    category = db.relationship('PartCategory', back_populates='parts')
    material = db.Column(db.String(64))
    status = db.Column(db.Integer)  # 0: Pending, 1: Completed
    revision = db.Column(db.String(32))
    updated_at = db.Column(db.DateTime)
    owner = db.Column(db.String(64))
    tolerance = db.Column(db.String(32))
    cad_file_url = db.Column(db.String(256))
    model_file_url = db.Column(db.String(256))
    description = db.Column(db.Text)
    standard = db.Column(db.String(64))
    specification = db.Column(db.Text)
    project_code = db.Column(db.String(64))
    drawing_number = db.Column(db.String(64))
