import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Kategorie_Wyceny, Pozycje_Wyceny
from werkzeug.security import generate_password_hash

# --- Ścieżki folderów, które mają istnieć ---
STATIC_FOLDERS = [
    os.path.join("static", "zdjecia"),
    os.path.join("static", "pdf")
]

# --- Utwórz bazę danych ---
engine = create_engine("sqlite:///baza.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# --- Dodaj domyślnego admina ---
def create_admin():
    if not session.query(User).filter_by(user_name="admin").first():
        admin = User(
            imie="Admin",
            nazwisko="Systemowy",
            user_name = "admin",
            rola="admin",
            haslo="admin"
        )
        session.add(admin)
        print("Dodano użytkownika admin")
    else:
        print("Użytkownik admin już istnieje.")


def create_kategorie():
    if not session.query(Kategorie_Wyceny).first():
        kat = [
            Kategorie_Wyceny("Typ schodów", "Schody policzkowe ażurowe", "Nowoczesne, lekkie wizualnie schody ażurowe wykonane z wysokiej jakości drewna dębowego. Konstrukcja grzebieniowa zapewnia trwałość i stabilność, a brak podstopnic dodaje wnętrzu przestronności. Idealne do nowoczesnych i klasycznych aranżacji."),
            Kategorie_Wyceny("Typ schodów", "Schody policzkowe pełne", "Nowoczesne, lekkie wizualnie schody pełne wykonane z wysokiej jakości drewna dębowego. Konstrukcja grzebieniowa zapewnia trwałość i stabilność. Idealne do nowoczesnych i klasycznych aranżacji."),
            Kategorie_Wyceny("Balustrady", "Balustrada Laserowa nr 37", "Dekoracyjna balustrada stalowa wycinana laserowo, osadzona w ramie z naturalnego drewna. Geometryczny, nieregularny wzór nadaje wnętrzu charakteru i podkreśla nowoczesny styl aranżacji.")
               ]
       
        session.add_all(kat)
        print("Dodano przykładowe kategorie.")

def create_pozycje():
    if not session.query(Pozycje_Wyceny).first():
        poz = [
            Pozycje_Wyceny(kategoria_id=1, pozycja="Stopień Ażur", cena_jednostkowa=1000.00, jednostka_miary="szt"),           
            Pozycje_Wyceny(kategoria_id=1, pozycja="Podest", cena_jednostkowa=900.00, jednostka_miary="m2"),
            Pozycje_Wyceny(kategoria_id=1, pozycja="Montaż schodów policzkowych", cena_jednostkowa=3000.00, jednostka_miary="kpl"),
            Pozycje_Wyceny(kategoria_id=2, pozycja="Stopień Pełne", cena_jednostkowa=1800.00, jednostka_miary="szt"),
            Pozycje_Wyceny(kategoria_id=2, pozycja="Podest", cena_jednostkowa=900.00, jednostka_miary="m2"),
            Pozycje_Wyceny(kategoria_id=2, pozycja="Montaż schodów policzkowych", cena_jednostkowa=3000.00, jednostka_miary="kpl"),
            Pozycje_Wyceny(kategoria_id=3, pozycja="Balustrada na antresoli ( prosta)", cena_jednostkowa=750.00, jednostka_miary="mb"),
               
               ]
        session.add_all(poz)
        print("➕ Dodano przykładową pozycję.")
    else:
        print("✔ Pozycje już istnieją.")

# --- Utwórz foldery static ---
def create_static_folders():
    for folder in STATIC_FOLDERS:
        os.makedirs(folder, exist_ok=True)
        print(f"📁 Upewniono się, że istnieje: {folder}")

# --- Uruchomienie całego setupu ---
def main():
    create_static_folders()
    create_admin()
    create_kategorie()
    create_pozycje()
    session.commit()
    session.close()
    print("✅ Baza danych gotowa do pracy.")

if __name__ == "__main__":
    main()