from flask_sqlalchemy import SQLAlchemy
import re

db = SQLAlchemy()

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

class PortfolioCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)  

    category = db.Column(db.String(120), nullable=False)
    category_slug = db.Column(db.String(200), nullable=False)      

    image = db.Column(db.String(255), nullable=True)

    tech1 = db.Column(db.String(120), nullable=True)
    tech2 = db.Column(db.String(120), nullable=True)
    year = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"<PortfolioCard {self.title}>"
