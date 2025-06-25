from flask import render_template, redirect, url_for, request, jsonify
from models import Wycena, Pozycje_Wyceny, Kategorie_Wyceny, Szczegoly_Wyceny
from run import app, session


@app.route("/szczegoly_wyceny/<int:wycid>", methods=["GET","POST"])
def szczegoly_wyceny(wycid):
    wycena = session.query(Wycena).get(wycid)
    szczegoly = session.query(Szczegoly_Wyceny).filter_by(wycid=wycid).all()
    sekcje = Kategorie_Wyceny.dict_kat_podkat(session)
    pozycje = session.query(Pozycje_Wyceny).all()


    suma = sum(s.cena_calkowita for s in szczegoly)

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