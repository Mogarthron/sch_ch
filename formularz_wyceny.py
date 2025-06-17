from run import *
from models import Wycena
from flask import request, render_template

@app.route("/formularz_wyceny", methods=["GET", "POST"]) #type: ignore
def formularz_wyceny():

    if request.method == "POST":
        form = request.form
        nowa_wycena = Wycena(form, session)

        session.add(nowa_wycena)
        session.commit()
    
    return render_template("formularz_wyceny.html")