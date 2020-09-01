"""Class-based Flask app configuration."""
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path='.env')

# SET dbtype to "psql" for using POSTGRESQL and "sqlite" for using SQLITE
dbtype = "sqlite"

if dbtype == "psql":
    db_url = f'postgresql://{os.getenv("dbuser_app")}:{os.getenv("dbpass_app")}@localhost/finapp'
elif dbtype == "sqlite":
    db_url = f'sqlite:///{os.getenv("dbname")}.sqlite3'

class Config:
    """Configuration from environment variables."""
    SECRET_KEY = os.getenv('SECRET_KEY_app')
    FLASK_APP = 'run.py'

    # Flask-Assets
    ASSETS_DEBUG = True
    LESS_RUN_IN_DEBUG = True

    # Static Assets
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    COMPRESSOR_DEBUG = True

   # Define the database - we are working with
    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
   # DATABASE_CONNECT_OPTIONS = {}

   # Application threads. A common general assumption is
   # using 2 per available processor cores - to handle
   # incoming requests using one and performing background
   # operations using the other.
    THREADS_PER_PAGE = 2

   # Enable protection agains *Cross-site Request Forgery (CSRF)*
   #CSRF_ENABLED     = True

   # Use a secure, unique and absolutely secret key for
   # signing the data.
   #CSRF_SESSION_KEY = "secret"

   # Allowed Extension files
    # ALLOWED_FILE_EXTENSIONS = ["XLS","CSV", "XLSX"]
    #
    #
    # UPLOAD_FOLDER = basedir+os.environ["stpath"]
