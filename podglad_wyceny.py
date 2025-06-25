from flask import render_template, redirect, url_for, request, jsonify, make_response
from models import Wycena, Pozycje_Wyceny, Kategorie_Wyceny, Szczegoly_Wyceny
from run import app, session
# from weasyprint import HTML
import os


@app.route("/podglad_wyceny/<wycid>", methods=["GET", "POST"])
def podglad_wyceny(wycid):

    wycena = session.query(Wycena).filter(Wycena.wycid == int(wycid)).first()
    sekcje = Kategorie_Wyceny.dict_kat_podkat(session)    

    return render_template("podglad_wyceny.html", wycena=wycena, sekcje=sekcje)

# @app.route("/drukuj_pdf/<int:wycid>")
# def drukuj_pdf(wycid):
#     wycena = session.query(Wycena).filter(Wycena.wycid == wycid).first()
#     sekcje = Kategorie_Wyceny.dict_kat_podkat(session)

#     # Pprzygotowanie ścieżki do zdjęć
#     zdjecia = {}
#     for sekcja in sekcje:
#         szczegoly_dla_sekcji = [
#             s for s in wycena.szczegoly
#             if s.pozycja and s.pozycja.kategoria_wyceny.nazwa_kategorii == sekcja
#         ]
#         if szczegoly_dla_sekcji:
#             zdjecie_url = szczegoly_dla_sekcji[0].pozycja.kategoria_wyceny.zdjecie_url
#             zdjecia[sekcja] = zdjecie_url  # np. 'zdjecia/typ_v.jpg'

#     # Renderowanie HTML
#     html = render_template(
#         "podglad_wyceny_pdf.html",
#         wycena=wycena,
#         sekcje=sekcje,
#         zdjecia=zdjecia  
#     )

#     # Ścieżka do pliku PDF
#     folder = os.path.join("static", "pdf")
#     os.makedirs(folder, exist_ok=True)
#     pdf_path = os.path.join(folder, f"wycena_{wycena.nr_zlecenia}.pdf")

#     # Grnerownie PDF
#     HTML(string=html, base_url=os.path.abspath("static")).write_pdf(pdf_path)

#     return redirect(url_for("podsumowanie_wycen"))