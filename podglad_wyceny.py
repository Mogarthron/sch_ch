from flask import render_template, redirect, url_for, request, jsonify
from models import Wycena, Pozycje_Wyceny, Kategorie_Wyceny, Szczegoly_Wyceny
from run import app, session


@app.route("/podglad_wyceny/<wycid>", methods=["GET", "POST"])
def podglad_wyceny(wycid):

    wycena = session.query(Wycena).filter(Wycena.wycid == int(wycid)).first()
    sekcje = Kategorie_Wyceny.dict_kat_podkat(session)

    

    return render_template("podglad_wyceny.html", wycena=wycena, sekcje=sekcje)