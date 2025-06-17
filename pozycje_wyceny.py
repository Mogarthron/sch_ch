from flask import request, render_template, redirect, url_for, jsonify

from models import *
from run import app, session



@app.route("/pozycje_wyceny", methods=["GET", "POST"])
def pozycje_wyceny():

    pozycje = session.query(Pozycje_Wyceny).all()

    return render_template("pozycje_wyceny.html", pozycje=pozycje)

@app.route("/pobierz_nazwy_podkategorii", methods=["GET"])
def pobierz_nazwy_podkategorii():
    wyniki = session.query(Kategorie_Wyceny.pod_kategoria).all() #type: ignore
    unikalne = [r[0] for r in wyniki]
    return jsonify(unikalne)

@app.route("/dodaj_pozycje_wyceny", methods=["POST"])
def dodaj_pozycje_wyceny():
    nazwa_kategorii = request.form.get("nazwa_kategorii")
    print(nazwa_kategorii)
    id_kat_wyceny = int(session.query(Kategorie_Wyceny.katid).filter(Kategorie_Wyceny.pod_kategoria == nazwa_kategorii).first()[0]) #type: ignore
    nazwa = request.form.get("nazwa_pozycji_wyceny")
    cena_jednostkowa = float(request.form.get("cena_jednostkowa")) #type: ignore
    jednostka_miary = request.form.get("jednostka_miary") 

    nowa_pozycja = Pozycje_Wyceny(
        kategoria_id=id_kat_wyceny,
        pozycja=nazwa,
        cena_jednostkowa=cena_jednostkowa,
        jednostka_miary=jednostka_miary
    )

    try:
        session.add(nowa_pozycja)
        session.commit()
        return redirect(url_for("dodaj_pozycje_wyceny"))
    except Exception as e:
        session.rollback()
        return jsonify(success=False, error=str(e)), 500


@app.route("/edytuj_pozycje_wyceny", methods=["GET", "POST"])
def edytuj_pozycje_wyceny():
    dane = request.get_json()
    try:
        poz = session.query(Pozycje_Wyceny).filter_by(cid=dane["cid"]).first()
        if not poz:
            return jsonify(success=False, error="Nie znaleziono pozycji")

        poz.pozycja = dane["pozycja"]
        poz.cena_jednostkowa = dane["cena_jednostkowa"]
        poz.jednostka_miary = dane["jednostka_miary"]
        session.commit()

        return jsonify(success=True)
    except Exception as e:
        session.rollback()
        return jsonify(success=False, error=str(e))