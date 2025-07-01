from app import create_app

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

engine = create_engine('sqlite:///baza.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

app = create_app()

from routs import *
from pozycje_wyceny import *
from formularz_wyceny import *
from kategorie_wyceny import *
from szczegoly_wyceny import *
from podglad_wyceny import *
from auth import *


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)