import uvicorn
from db.models import setup_database
from api.api import app

setup_database()