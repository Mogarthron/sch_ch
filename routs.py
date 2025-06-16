from app import os
from flask import request, render_template, redirect, url_for, jsonify
from werkzeug.utils import secure_filename

from models import *
from run import app



@app.route("/")
def index():
    return render_template("index.html")


@app.route('/formularz_oferty', methods=['GET', 'POST'])
def formularz_oferty():

    typy_schodow = [file.split('.')[0] for file in os.listdir("./static/typy_schodow")]
    wykonczenie_schodow = [file.split('.')[0] for file in os.listdir("./static/wykonczenie_schodow")]
    typ_balustrady = [file.split('.')[0] for file in os.listdir("./static/typ_balustrady")]
    obrobka_stropu = [file.split('.')[0] for file in os.listdir("./static/obrobka_stropu")]
    polaczenie_z_posadzka = [file.split('.')[0] for file in os.listdir("./static/polaczenie_z_posadzka")]

    if request.method == "POST":
        nowa_oferta = Oferta.from_form(request.form)
        session.add(nowa_oferta)
        session.commit()

        return redirect(url_for("oferta", nr_zlecenia=request.form["nr_zlecenia"]))

    return render_template('formularz_oferty.html', typy_schodow=typy_schodow, 
                                                    wykonczenie_schodow=wykonczenie_schodow,
                                                    typ_balustrady=typ_balustrady,
                                                    obrobka_stropu=obrobka_stropu,
                                                    polaczenie_z_posadzka=polaczenie_z_posadzka)

@app.route('/oferta/<nr_zlecenia>', methods=['GET', 'POST'])
def oferta(nr_zlecenia):

    
    _dane = session.query(Oferta).filter_by(nr_zlecenia=nr_zlecenia).first()
    dane = _dane.to_dict() # type: ignore
    print(dane)

    
    return render_template('oferta.html', dane=dane)

@app.route("/podsumowanie_wycen", methods=["GET", "POST"])
def podsumowanie_wycen():
    
    wyceny = (
        session.query(Wycena).all()
    )

    if request.method=="POST":
        wycid = int(request.form.get("wycid")) #type: ignore
        
        return redirect(url_for("szczegoly_wyceny", wycid=wycid))


    return render_template("podsumowanie_wycen.html", wyceny=wyceny)


@app.route("/wyslano_oferte", methods=["POST"])
def wyslano_oferte():
    dane = request.get_json()
    nr = dane.get("nr_zlecenia")

    try:
        oferta = session.query(Oferta).filter_by(nr_zlecenia=nr).first()
        if not oferta:
            return jsonify(success=False, error="Nie znaleziono oferty")

        oferta.data_wyslania = dt.now().date() #type: ignore
        oferta.status_zlecenia = "Wysłano" #type: ignore
        session.commit()

        return jsonify(success=True, data_wyslania=str(oferta.data_wyslania))

    except Exception as e:
        session.rollback()
        return jsonify(success=False, error=str(e))


@app.route("/szczegoly_oferty/<nr_zlecenia>", methods=["GET", "POST"])
def szeczegoly_oferty(nr_zlecenia):

    oferta_naglowek = session.query(Oferta).filter(Oferta.nr_zlecenia==nr_zlecenia).first()
    
    wiersze_oferty = (
    session.query(Oferta_Szczegoly)
    .filter(Oferta_Szczegoly.oferta_id == oferta_naglowek.zamid) #type: ignore
    .all()
    )

    return render_template("szczegoly_oferty.html", 
                           oferta_naglowek=oferta_naglowek.to_dict(), # type: ignore
                           wiersze_oferty=wiersze_oferty,
                           
                           ) 

@app.route("/szczegoly_oferty_edytuj_wiersz", methods=["POST"])
def szczegoly_oferty_edytuj_wiersz():
    dane = request.get_json()
    wiersz_id = dane.get("id")
    nowa_opis = dane.get("opis")
    nowa_ilosc = dane.get("ilosc")
    nowa_cena = dane.get("cena")

    try:
        wiersz = session.query(Oferta_Szczegoly).get(wiersz_id)
        if not wiersz:
            return jsonify(success=False, error="Nie znaleziono wiersza")

        wiersz.opis = nowa_opis
        wiersz.ilosc = nowa_ilosc.replace(",", ".")
        wiersz.cena = nowa_cena.replace(",", ".")
        session.commit()
        return jsonify(success=True)

    except Exception as e:
        session.rollback()
        return jsonify(success=False, error=str(e))

@app.route("/oferta_szczegoly/<nr_zlecenia>", methods=["POST"])
def zapisz_szczegoly(nr_zlecenia):
    oferta = session.query(Oferta).filter_by(nr_zlecenia=nr_zlecenia).first()
    if not oferta:
        return "Oferta nie istnieje", 404

    dane = request.get_json()
    sekcja = dane.get("sekcja")
    wiersze = dane.get("wiersze")

    if not wiersze or not isinstance(wiersze, list):
        return "Nieprawidłowe dane wejściowe", 400

    for poz in wiersze:
        # Dodaj sekcję do każdego wiersza (bo jest wspólna)
        szczegol = Oferta_Szczegoly.from_dict({**poz, "sekcja": sekcja}, oferta_id=oferta.zamid) # type: ignore
        session.add(szczegol)

    session.commit()
    return "Zapisano szczegóły", 200