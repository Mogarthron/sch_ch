from app import create_app

app = create_app()

from routs import *
from pozycje_wyceny import *
from formularz_wyceny import *
from kategorie_wyceny import *
from szczegoly_wyceny import *


if __name__ == '__main__':
    app.run(debug=True)