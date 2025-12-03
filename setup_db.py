import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Handlowiec, Kategorie_Wyceny, Pozycje_Wyceny
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
        users = [
            User(imie="Admin", nazwisko="Systemowy", user_name = "admin", rola="admin", haslo="admin"),
            User(imie="Handlowiec", nazwisko="Jeden", user_name = "han1", rola="pracownik biuro", haslo="qwerty"),            
            ]
        session.add_all(users)
        print("Dodano użytkownika admin")
    else:
        print("Użytkownik admin już istnieje.")

def create_handlowiec():
    handl = [
            Handlowiec(user_id=2, nr_kontaktowy="666555666", email="han1_@poczta.com.pl"),
                      
            ]
    session.add_all(handl)
    print("Dodano handlowca")

# --- Utwórz foldery static ---
def create_static_folders():
    for folder in STATIC_FOLDERS:
        os.makedirs(folder, exist_ok=True)
        print(f"📁 Upewniono się, że istnieje: {folder}")

# --- Uruchomienie całego setupu ---
def main():
    create_static_folders()
    create_admin()
    create_handlowiec()

    session.commit()
    session.close()
    print("✅ Baza danych gotowa do pracy.")

if __name__ == "__main__":
    main()