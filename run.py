from app import app, db
from app.models import User

@app.shell_context_processor
def make_context():
    return {"User": User, "db": db}