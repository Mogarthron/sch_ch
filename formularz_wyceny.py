from run import *
from models import Wycena
from flask import request, render_template
from flask_login import current_user
from auth import login_required

@app.route("/formularz_wyceny", methods=["GET", "POST"]) #type: ignore
@login_required
def formularz_wyceny():
    
    if request.method == "POST":
        form = request.form
        nowa_wycena = Wycena(form, session, current_user.handlowiec.handlowiec_id)

        session.add(nowa_wycena)
        session.commit()
    
    return render_template("formularz_wyceny.html")