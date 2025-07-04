from flask import render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import os

from models import Kategorie_Wyceny

from run import app, session


@app.route("/kategorie_wyceny", methods=["GET", "POST"])
def kategorie_wyceny():

    kategorie = session.query(Kategorie_Wyceny).order_by(Kategorie_Wyceny.nazwa_kategorii).all() #type: ignore

    return render_template("kategorie_wyceny.html", kategorie=kategorie)

def allowed_file(filename):

    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {"png", "jpg", "jpeg", "gif"}

@app.route("/dodaj_kategorie_wyceny", methods=["POST"])
def dodaj_kategorie_wyceny():
    nazwa_kategorii = request.form.get("nazwa_kategorii")
    pod_kategoria = request.form.get("nazwa_podkategorii")
    opis_kategorii = request.form.get("opis_kategorii")
    plik = request.files.get("zdjecie")

    zdjecie_url = None
    if plik and plik.filename:
        filename = secure_filename(plik.filename)
        filepath = os.path.join("static", "zdjecia", filename)
        plik.save(filepath)
        zdjecie_url = f"zdjecia/{filename}"

    nowa_kategoria = Kategorie_Wyceny(
        nazwa_kategorii=nazwa_kategorii,
        pod_kategoria=pod_kategoria,
        opis_kategorii=opis_kategorii,
        zdjecie_url=zdjecie_url
    )

    try:
        session.add(nowa_kategoria)
        session.commit()
        return redirect(url_for("dodaj_kategorie_wyceny"))
    except Exception as e:
        session.rollback()

        return jsonify(success=False, error=str(e)), 500

@app.route("/pobierz_nazwy_kategorii", methods=["GET"])
def pobierz_nazwy_kategorii():
    wyniki = session.query(Kategorie_Wyceny.nazwa_kategorii).distinct().all() #type: ignore
    unikalne = [r[0] for r in wyniki]

    return jsonify(unikalne)

@app.route("/edytuj_kategorie_wyceny", methods=["POST"])
def edytuj_kategorie_wyceny():
    
    katid = request.form.get("katid")
    nowa_nazwa = request.form.get("nazwa_kategorii")
    nowy_opis = request.form.get("opis_kategorii")
    nowe_zdjecie = request.files.get("zdjecie")

    kat = session.query(Kategorie_Wyceny).get(katid)

    if not kat:
        return jsonify(success=False, error="Nie znaleziono kategorii")

    kat.nazwa_kategorii = nowa_nazwa
    kat.opis_kategorii = nowy_opis

    if nowe_zdjecie and nowe_zdjecie.filename:
        # Usuń stare zdjęcie jeśli istnieje
        if kat.zdjecie_url:
            stara_sciezka = os.path.join(app.root_path, kat.zdjecie_url.strip("/"))
            if os.path.exists(stara_sciezka):
                os.remove(stara_sciezka)

        # Zapisz nowe zdjęcie
        filename = secure_filename(nowe_zdjecie.filename)
        folder = os.path.join(app.root_path, "static", "zdjecia")
        os.makedirs(folder, exist_ok=True)
        sciezka_zapisu = os.path.join(folder, filename)
        nowe_zdjecie.save(sciezka_zapisu)

        kat.zdjecie_url = f"zdjecia/{filename}"

    try:
        session.commit()
        return jsonify(success=True, zdjecie_url=kat.zdjecie_url)
    except Exception as e:
        session.rollback()
        
        return jsonify(success=False, error=str(e)), 500
