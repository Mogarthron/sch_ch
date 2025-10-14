from flask import render_template, redirect, url_for, request, jsonify,abort
from sqlalchemy.orm import joinedload
from models import Wycena, Pozycje_Wyceny, Kategorie_Wyceny, Szczegoly_Wyceny
from run import app, session


@app.route("/szczegoly_wyceny/<int:wycid>", methods=["GET","POST"])
def szczegoly_wyceny(wycid):
    wycena = session.query(Wycena).get(wycid)
    szczegoly = session.query(Szczegoly_Wyceny).filter_by(wycid=wycid).all()
    sekcje = Kategorie_Wyceny.dict_kat_podkat(session)
    pozycje = session.query(Pozycje_Wyceny).order_by(Pozycje_Wyceny.pozycja).all()


    suma = sum(s.cena_calkowita for s in szczegoly)
    suma_mat = sum(s.cena_materialu for s in szczegoly)

    if request.method == "POST":
        szczegol_wyceny = Szczegoly_Wyceny(request.form, wycid, session)
        session.add(szczegol_wyceny)
        session.commit()

        # print(request.form)

        return redirect(url_for("szczegoly_wyceny", wycid=wycid))

    return render_template("szczegoly_wyceny.html", 
                            wycena=wycena,
                            sekcje=sekcje,
                            szczegoly=szczegoly,
                            suma_wyceny=suma,
                            suma_materialow=suma_mat,
                            # pozycje=pozycje
                            )


@app.route("/api/podkategorie_pozycje", methods=["GET", "POST"])
def podkategorie_pozycje():
    """
    funkacja api która przekazuje pary podkategorie - pozycje do modala dodającego szczegół wyceny
    """
    podkategoria = request.args.get("podkategoria")
    pozycje_podkategorii = session.query(Pozycje_Wyceny.cid, Pozycje_Wyceny.pozycja).join(Kategorie_Wyceny).filter(Kategorie_Wyceny.pod_kategoria == podkategoria).all()
    print(podkategoria, pozycje_podkategorii)

    return jsonify([{"id": p.cid, "nazwa": p.pozycja} for p in pozycje_podkategorii])



@app.route("/api/szczegoly_wyceny/update", methods=["POST"])
def update_szczegoly_wyceny():
    """
    funkcja updatujaca pola indywidualna nazwa, dodatkowy opis, ilosc, cena całkowita
    """
    data = request.get_json()
    szwycid = data.get("szwycid")

    szczegol = session.query(Szczegoly_Wyceny).get(szwycid)
    if not szczegol:
        return jsonify({"success": False, "error": "Nie znaleziono wiersza"}), 404

    szczegol.indywidualna_nazwa = data.get("indywidualna_nazwa", None)
    szczegol.dodatkowy_opis = data.get("dodatkowy_opis", "")
    szczegol.ilosc = data.get("ilosc", 0)
    szczegol.cena_calkowita = data.get("cena_calkowita", 0)

    session.commit()

    jednostka = szczegol.pozycja.jednostka_miary if szczegol.pozycja else ""

    return jsonify({"success": True, "jednostka": jednostka})


@app.route("/api/szczegoly_wyceny/delete/<int:szwycid>", methods=["DELETE"])
def delete_szczegol_wyceny(szwycid):
    szczegol = session.query(Szczegoly_Wyceny).get(szwycid)
    if not szczegol:
        return jsonify({"success": False, "error": "Nie znaleziono wiersza"}), 404

    session.delete(szczegol)
    session.commit()
    return jsonify({"success": True})


from flask import request, jsonify

@app.post("/api/wycena/<int:wycid>/update")
def api_update_wycena(wycid):
    wycena = session.get(Wycena, wycid)
    if not wycena:
        return jsonify(success=False, error="Nie znaleziono wyceny"), 404

    data = request.get_json() or {}

    # Aktualizowane pola
    wycena.imie_klienta      = data.get("imie_klienta")      or wycena.imie_klienta
    wycena.nazwisko_klienta  = data.get("nazwisko_klienta")  or wycena.nazwisko_klienta
    wycena.ulica             = data.get("ulica")             or wycena.ulica
    wycena.numer_domu        = data.get("numer_domu")        or wycena.numer_domu
    wycena.kod_pocztowy      = data.get("kod_pocztowy")      or wycena.kod_pocztowy
    wycena.miasto            = data.get("miasto")            or wycena.miasto
    wycena.kontakt_telefon   = data.get("kontakt_telefon")   or wycena.kontakt_telefon
    wycena.kontakt_email     = data.get("kontakt_email")     or wycena.kontakt_email
    wycena.nr_zlecenia       = data.get("nr_zlecenia")       or wycena.nr_zlecenia

    try:
        session.commit()
    except Exception as e:
        session.rollback()
        return jsonify(success=False, error=str(e)), 500

    # Zwracamy to, co front od razu wstawi na stronę (live-update)
    return jsonify(
        success=True,
        wycid=wycena.wycid,
        imie_klienta=wycena.imie_klienta,
        nazwisko_klienta=wycena.nazwisko_klienta,
        ulica=wycena.ulica,
        numer_domu=wycena.numer_domu,
        kod_pocztowy=wycena.kod_pocztowy,
        miasto=wycena.miasto,
        kontakt_telefon=wycena.kontakt_telefon,
        kontakt_email=wycena.kontakt_email,
        nr_zlecenia=wycena.nr_zlecenia,
    )

@app.get("/szczegoly_wyceny/<int:wycid>/podsumowanie")
def podsumowanie_widok(wycid):
    wycena = session.get(Wycena, wycid)
    if not wycena:
        abort(404)

    szczegoly = (
        session.query(Szczegoly_Wyceny)
        .options(
            joinedload(Szczegoly_Wyceny.pozycja)
            .joinedload(Pozycje_Wyceny.kategoria_wyceny)
        )
        .filter(Szczegoly_Wyceny.wycid == wycid)
        .all()
    )
   
    s = wycena.podsumowanie_wyceny()

    return render_template(
        "podsumowanie_wyceny.html",
        wycena=wycena,
        s=s,
        szczegoly=szczegoly,
    )