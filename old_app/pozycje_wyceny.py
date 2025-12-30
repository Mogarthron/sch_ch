from flask import request, render_template, redirect, url_for, jsonify

from models import *
from run import app, session
import os
from werkzeug.utils import secure_filename

UPLOAD_POZYCJE_DIR = os.path.join(app.root_path, "static", "zdjecia", "pozycje")
os.makedirs(UPLOAD_POZYCJE_DIR, exist_ok=True)



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
    id_kat_wyceny = int(
        session.query(Kategorie_Wyceny.katid)
        .filter(Kategorie_Wyceny.pod_kategoria == nazwa_kategorii)
        .first()[0]  # type: ignore
    )

    nazwa = request.form.get("nazwa_pozycji_wyceny")
    cena_jednostkowa = float(request.form.get("cena_jednostkowa") or 0)
    jednostka_miary = request.form.get("jednostka_miary")

    # obsługa pliku
    plik = request.files.get("zdjecie")
    zdjecie_url = None
    if plik and plik.filename:
        filename = secure_filename(plik.filename)
        sciezka_fs = os.path.join(UPLOAD_POZYCJE_DIR, filename)
        plik.save(sciezka_fs)
        # ścieżka względna względem katalogu static
        zdjecie_url = f"zdjecia/pozycje/{filename}"

    nowa_pozycja = Pozycje_Wyceny(
        kategoria_id=id_kat_wyceny,
        pozycja=nazwa,
        cena_jednostkowa=cena_jednostkowa,
        jednostka_miary=jednostka_miary,
        zdjecie_url=zdjecie_url,
    )

    try:
        session.add(nowa_pozycja)
        session.commit()
        return jsonify(success=True)
    except Exception as e:
        session.rollback()
        return jsonify(success=False, error=str(e)), 500

# @app.route("/dodaj_pozycje_wyceny", methods=["POST"])
# def dodaj_pozycje_wyceny():
#     nazwa_kategorii = request.form.get("nazwa_kategorii")
#     print(nazwa_kategorii)
#     id_kat_wyceny = int(session.query(Kategorie_Wyceny.katid).filter(Kategorie_Wyceny.pod_kategoria == nazwa_kategorii).first()[0]) #type: ignore
#     nazwa = request.form.get("nazwa_pozycji_wyceny")
#     cena_jednostkowa = float(request.form.get("cena_jednostkowa")) #type: ignore
#     jednostka_miary = request.form.get("jednostka_miary") 

#     nowa_pozycja = Pozycje_Wyceny(
#         kategoria_id=id_kat_wyceny,
#         pozycja=nazwa,
#         cena_jednostkowa=cena_jednostkowa,
#         jednostka_miary=jednostka_miary
#     )

#     try:
#         session.add(nowa_pozycja)
#         session.commit()
#         return redirect(url_for("dodaj_pozycje_wyceny"))
#     except Exception as e:
#         session.rollback()
#         return jsonify(success=False, error=str(e)), 500


# @app.route("/edytuj_pozycje_wyceny", methods=["GET", "POST"])
# def edytuj_pozycje_wyceny():
#     dane = request.get_json()
#     try:
#         poz = session.query(Pozycje_Wyceny).filter_by(cid=dane["cid"]).first()
#         if not poz:
#             return jsonify(success=False, error="Nie znaleziono pozycji")

#         poz.pozycja = dane["pozycja"]
#         poz.cena_jednostkowa = dane["cena_jednostkowa"]
#         poz.cena_materialu = dane["cena_materialu"]
#         poz.jednostka_miary = dane["jednostka_miary"]
#         poz.zdjecie_url = dane["zdjecie_url"] or None
#         session.commit()

#         return jsonify(success=True)
#     except Exception as e:
#         session.rollback()
#         return jsonify(success=False, error=str(e))

@app.route("/edytuj_pozycje_wyceny", methods=["POST"])
def edytuj_pozycje_wyceny():
    try:
        cid = int(request.form.get("cid"))
        poz = session.query(Pozycje_Wyceny).filter_by(cid=cid).first()
        if not poz:
            return jsonify(success=False, error="Nie znaleziono pozycji")

        # pola tekstowe
        poz.pozycja = request.form.get("pozycja")
        poz.cena_jednostkowa = request.form.get("cena_jednostkowa") or 0
        poz.cena_materialu = request.form.get("cena_materialu") or 0
        poz.jednostka_miary = request.form.get("jednostka_miary")

        # plik (opcjonalnie)
        plik = request.files.get("zdjecie")
        if plik and plik.filename:
            filename = secure_filename(plik.filename)
            sciezka_fs = os.path.join(UPLOAD_POZYCJE_DIR, filename)
            plik.save(sciezka_fs)
            poz.zdjecie_url = f"zdjecia/pozycje/{filename}"  # ścieżka względem /static

        session.commit()
        return jsonify(success=True, zdjecie_url=poz.zdjecie_url)
    except Exception as e:
        session.rollback()
        return jsonify(success=False, error=str(e)), 500