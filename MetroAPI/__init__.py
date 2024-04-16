from os import getenv
from dotenv import load_dotenv

from flask import Flask

from MetroAPI.handlers.metro import start_service


load_dotenv()
DEBUG = getenv('DEBUG')
IP = getenv('IP')
PORT = getenv('PORT')
# start_service()


app = Flask(__name__, template_folder='templates')

from .routes import main_routes

