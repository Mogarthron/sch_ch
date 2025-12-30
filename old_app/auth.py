from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from models import User, Handlowiec
from app import login_manager
from run import session, app



@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(int(user_id))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_name = request.form.get("user_name")
        haslo = request.form.get("haslo")

        user = session.query(User).filter_by(user_name=user_name).first()
        if user and user.check_password(haslo):
            login_user(user)
            return redirect(url_for("podsumowanie_wycen"))  # lub inny domyślny widok
        else:
            flash("Nieprawidłowe dane logowania", "danger")

    return render_template("login.html")



@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Wylogowano pomyślnie", "success")
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            user = User.from_form(request.form, session)
            session.add(user)
            session.commit()
            flash("Użytkownik utworzony pomyślnie.", "success")
            return redirect(url_for("login"))  # zmień jeśli inna nazwa
        except Exception as e:
            session.rollback()
            flash(f"Błąd: {str(e)}", "danger")

    return render_template("register.html")

@app.route("/uzytkownicy")
@login_required
def lista_uzytkownikow():
    if current_user.rola != "admin":
        flash("Brak dostępu.", "danger")
        return redirect(url_for("login"))
    uzytkownicy = session.query(User).all()
    return render_template("lista_uzytkownikow.html", uzytkownicy=uzytkownicy)

@app.route("/edytuj_uzytkownika/<int:user_id>", methods=["GET", "POST"])
@login_required
def edytuj_uzytkownika(user_id):
    if current_user.rola != "admin":
        flash("Brak dostępu.", "danger")
        return redirect(url_for("login"))

    user = session.query(User).get(user_id)
    if not user:
        flash("Nie znaleziono użytkownika.", "warning")
        return redirect(url_for("lista_uzytkownikow"))

    if request.method == "POST":
        user.imie = request.form.get("imie")
        user.nazwisko = request.form.get("nazwisko")
        user.rola = request.form.get("rola")
        user.monday_api = request.form.get("monday_api")

        if request.form.get("haslo"):
            user.set_password(request.form.get("haslo"))

        session.commit()
        flash("Zaktualizowano dane użytkownika.", "success")
        return redirect(url_for("lista_uzytkownikow"))

    return render_template("edytuj_uzytkownika.html", user=user)

@app.route("/dodaj_handlowca", methods=["GET", "POST"])
@login_required
def dodaj_handlowca():
    if current_user.rola != "admin":
        flash("Brak uprawnień do dodawania handlowców.", "danger")
        return redirect(url_for("lista_handlowcow"))

    uzytkownicy = session.query(User).filter(~User.handlowiec.has()).all()  # tylko ci, którzy nie są jeszcze handlowcami

    if request.method == "POST":
        user_id = request.form.get("user_id")
        email = request.form.get("email")
        telefon = request.form.get("telefon")

        if not (user_id and email and telefon):
            flash("Wszystkie pola są wymagane.", "warning")
            return redirect(request.url)

        # upewnij się, że user istnieje
        user = session.query(User).filter_by(user_id=int(user_id)).first()
        if not user:
            flash("Wybrany użytkownik nie istnieje.", "danger")
            return redirect(request.url)

        # sprawdź czy nie ma już przypisanego handlowca
        if user.handlowiec:
            flash("Ten użytkownik już jest handlowcem.", "warning")
            return redirect(request.url)

        handlowiec = Handlowiec(user_id=user.user_id, email=email, nr_kontaktowy=telefon)
        session.add(handlowiec)
        session.commit()
        flash("Dodano nowego handlowca.", "success")
        return redirect(url_for("lista_handlowcow"))

    return render_template("dodaj_handlowca.html", uzytkownicy=uzytkownicy)


@app.route("/handlowcy")
@login_required
def lista_handlowcow():
    if current_user.rola != "admin":
        flash("Brak dostępu tylko administrator.", "danger")
        return redirect(url_for("formularz_wyceny"))

    handlowcy = session.query(Handlowiec).all()
    return render_template("lista_handlowcow.html", handlowcy=handlowcy)

@app.route("/edytuj_handlowca/<int:handlowiec_id>", methods=["GET", "POST"])
@login_required
def edytuj_handlowca(handlowiec_id):
    if current_user.rola != "admin":
        flash("Brak dostępu – tylko administrator.", "danger")
        return redirect(url_for("formularz_wyceny"))

    handlowiec = session.query(Handlowiec).filter_by(handlowiec_id=handlowiec_id).first()

    if not handlowiec:
        flash("Nie znaleziono handlowca.", "danger")
        return redirect(url_for("lista_handlowcow"))

    if request.method == "POST":
        form = request.form
        handlowiec.user.imie = form.get("imie")
        handlowiec.user.nazwisko = form.get("nazwisko")
        handlowiec.user.user_name = form.get("user_name")
        handlowiec.email = form.get("email")
        handlowiec.nr_kontaktowy = form.get("nr_kontaktowy")

        session.commit()
        flash("Dane handlowca zaktualizowane.", "success")
        return redirect(url_for("lista_handlowcow"))

    return render_template("edytuj_handlowca.html", h=handlowiec)

@app.route("/usun_handlowca/<int:handlowiec_id>")
@login_required
def usun_handlowca(handlowiec_id):
    if current_user.rola != "admin":
        flash("Brak uprawnień do usuwania handlowców.", "danger")
        return redirect(url_for("lista_handlowcow"))

    handlowiec = session.query(Handlowiec).filter_by(handlowiec_id=handlowiec_id).first()

    if not handlowiec:
        flash("Handlowiec nie istnieje.", "warning")
        return redirect(url_for("lista_handlowcow"))

    session.delete(handlowiec.user)  # Usuwa również handlowca przez relację
    session.commit()
    flash("Handlowiec usunięty.", "success")
    return redirect(url_for("lista_handlowcow"))

@app.route("/reset_hasla/<int:user_id>", methods=["GET", "POST"])
@login_required
def reset_hasla(user_id):
    if current_user.rola != "admin":
        flash("Brak dostępu do resetowania haseł.", "danger")
        return redirect(url_for("lista_handlowcow"))

    user = session.query(User).filter_by(user_id=user_id).first()

    if not user:
        flash("Użytkownik nie znaleziony.", "warning")
        return redirect(url_for("lista_handlowcow"))

    if request.method == "POST":
        nowe_haslo = request.form.get("haslo")
        if not nowe_haslo:
            flash("Hasło nie może być puste.", "warning")
            return redirect(request.url)

        user.set_password(nowe_haslo)
        session.commit()
        flash("Hasło zresetowane.", "success")
        return redirect(url_for("lista_handlowcow"))

    return render_template("reset_hasla.html", user=user)