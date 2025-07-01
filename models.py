from sqlalchemy import Column, Integer, Numeric, Float, String, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime as dt
from sqlalchemy import func, cast, Float, Integer
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_login import UserMixin

from collections import defaultdict

Base = declarative_base()

class User(Base, UserMixin):
    __tablename__ = "user"

    user_role = {
        1: "admin",
        2: "kierownik",
        3: "pracownik biuro",
        4: "procownik produkcja"

    }

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(128), nullable=False, unique=True)
    imie = Column(String(128), nullable=False)
    nazwisko = Column(String(128), nullable=False)
    rola = Column(String(68), nullable=False)
    haslo_hash = Column(String(128), nullable=False)
    aktywny = Column(Boolean, default=True)

    handlowiec = relationship("Handlowiec", back_populates="user", cascade="all, delete-orphan", uselist=False)

    def __init__(self, imie, nazwisko, user_name, rola, haslo):
        self.imie = imie
        self.nazwisko = nazwisko
        self.user_name = user_name
        self.rola = rola
        self.set_password(haslo)

    def set_password(self, haslo):
        self.haslo_hash = generate_password_hash(haslo)

    def check_password(self, haslo):
        return check_password_hash(self.haslo_hash, haslo)
    
    def get_id(self):
        return str(self.user_id)
    
    def dezaktywoj_usera(self):
        if self.aktywny:
            self.aktywny = False

    @classmethod
    def from_form(cls, form, session):
       
        # Sprawdzenie, czy użytkownik już istnieje
        user_name = form.get("user_name")

        existing_user = session.query(cls).filter_by(user_name=user_name).first()
        if existing_user:
            raise ValueError(f"Użytkownik '{user_name}' już istnieje.")
        
        return cls(
            user_name=form.get("user_name"),
            imie=form.get("imie"),
            nazwisko=form.get("nazwisko"),
            rola=form.get("rola"),
            haslo=form.get("haslo")
        )

class Handlowiec(Base):
    __tablename__ = "handlowiec"

    handlowiec_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    nr_kontaktowy = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)

    user = relationship("User", back_populates="handlowiec")
    wyceny = relationship("Wycena", back_populates="handlowiec", cascade="all, delete-orphan")
    

class Kategorie_Wyceny(Base):
    __tablename__ = "kategorie_wyceny"

    katid = Column(Integer, primary_key=True)
    nazwa_kategorii = Column(String(128), nullable=False) #typ schodów, balustrady
    pod_kategoria = Column(String(128), nullable=False) #np. schody policzkowe, schody grzebieniowe, tralka 15
    opis_kategorii = Column(String(256))
    zdjecie_url = Column(String(256))

    pozycje_wyceny = relationship("Pozycje_Wyceny", back_populates="kategoria_wyceny", cascade="all, delete-orphan")
    
    def __init__(self, nazwa_kategorii, pod_kategoria, opis_kategorii=None, zdjecie_url=None):
        self.nazwa_kategorii = nazwa_kategorii
        self.pod_kategoria = pod_kategoria
        self.opis_kategorii = opis_kategorii  
        self.zdjecie_url = zdjecie_url

    @classmethod
    def from_form(cls, form):       

        return cls(
            nazwa_kategorii=form.get("nazwa_kategorii"),
            pod_kategoria = form.get("pod_kategoria"),
            opis_kategorii=form.get("opis_kategorii"),
            zdjecie_url=form.get("zdjecie")
        )
    
    @classmethod
    def dict_kat_podkat(cls, session):
        """
        Zwraca słownik {"nazwa_kategorii": [lista podkategorii]}
        """
        kategorie = session.query(cls.nazwa_kategorii, cls.pod_kategoria).all()
        wynik = {}

        for nazwa_kategorii, pod_kategoria in kategorie:
            wynik.setdefault(nazwa_kategorii, []).append(pod_kategoria)

        return wynik


class Pozycje_Wyceny(Base):
    __tablename__ = "pozycje_wyceny"

    cid = Column(Integer, primary_key=True)
    kategoria_id = Column(Integer, ForeignKey('kategorie_wyceny.katid'), nullable=False) # Typ schodó, balustrada itd
    pozycja = Column(String(128), nullable=False)
    cena_jednostkowa = Column(Numeric(10,2))
    jednostka_miary = Column(String(16))
    data_wprowadzenia = Column(DateTime, default=dt.now)
    data_edycji = Column(DateTime, default=dt.now, onupdate=dt.now)

    kategoria_wyceny = relationship("Kategorie_Wyceny", back_populates="pozycje_wyceny")
    
    

    def __init__(self, kategoria_id:int, pozycja, cena_jednostkowa, jednostka_miary):
        self.kategoria_id = kategoria_id
        self.pozycja = pozycja
        self.cena_jednostkowa = cena_jednostkowa
        self.jednostka_miary = jednostka_miary
      
    @classmethod
    def from_form(cls, form, kategoria_id:int):

        return cls(
            kategoria_id = kategoria_id,
            pozycja = form.get("pozycja"),
            cena_jednostkowa = form.get("cena_jednostkowa"),
            jednostka_miary = form.get("jednostka_miary"),
        )

class Wycena(Base):
    __tablename__ = "wycena"

    opcje_statusu = {
                        1: "Wprowadzone",
                        2: "Wysłane",
                        3: "Zaakceptowane",
                        4: "Odrzucone"
                     }

    wycid = Column(Integer, primary_key=True)
    handlowiec_id = Column(Integer, ForeignKey('handlowiec.handlowiec_id'), nullable=True)
    rok = Column(Integer)
    kolejny_numer = Column(Integer)
    nr_zlecenia = Column(String(64), nullable=False, unique=True)
    imie_klienta = Column(String(128), nullable=False)
    nazwisko_klienta = Column(String(128), nullable=False)
    data_wprowadzenia = Column(DateTime, default=dt.now)
    numer_domu = Column(String(256))
    ulica = Column(String(256))
    miasto = Column(String(256))
    kod_pocztowy = Column(String(16))
    kontakt_telefon = Column(String(64))
    kontakt_email = Column(String(128))
    
    status_wyceny = Column(String, default="Wprowadzone")
    data_wyslania = Column(DateTime, nullable=True)
    powod_odrzucenia = Column(String)
    dodatkowe_uwagi = Column(String)
    data_zamkniecia = Column(DateTime, nullable=True) #Data zaakceptowania lub odrzucenia wyceny, po tej dacie powinno się wysłąć odertę

    szczegoly = relationship("Szczegoly_Wyceny", back_populates="wycena", cascade="all, delete-orphan")
    handlowiec = relationship("Handlowiec", back_populates="wyceny")

    def __init__(self, form, session, handlowiec_id):

        self.rok = dt.now().year
        # kolejny numer w danym roku:
        ostatni_numer = session.query(Wycena.kolejny_numer).filter(Wycena.rok == self.rok).order_by(Wycena.kolejny_numer.desc()).first() #type: ignore

        self.kolejny_numer = (ostatni_numer[0] + 1) if ostatni_numer else 1
        self.nr_zlecenia = f"{self.rok}_{self.kolejny_numer:03d}"

        # Dane z formularza
        self.imie_klienta = form.get("imie_klienta")
        self.nazwisko_klienta = form.get("nazwisko_klienta")
        self.handlowiec_id = handlowiec_id
        self.numer_domu = form.get("numer_domu")
        self.ulica = form.get("ulica")
        self.miasto = form.get("miasto")
        self.kod_pocztowy = form.get("kod_pocztowy")
        self.kontakt_telefon = form.get("kontakt_telefon")
        self.kontakt_email = form.get("kontakt_email")
        self.dodatkowe_uwagi = form.get("dodatkowe_uwagi")

    @property
    def adres_inwestycji(self):

        return f"{self.ulica} {self.numer_domu}, {self.kod_pocztowy} {self.miasto}"

    @property
    def wartosc_calkowita(self):

        return sum(s.cena_calkowita or 0 for s in self.szczegoly)
    
    @property
    def wartosc_podsumowanie_kategorii(self):
        """
        Zwraca słownik {"kategoria": suma} na podstawie szczegółów wyceny.
        """
        podsumowanie = defaultdict(float)

        for szczegol in self.szczegoly:
            if szczegol.pozycja and szczegol.pozycja.kategoria_wyceny:
                nazwa_kategorii = szczegol.pozycja.kategoria_wyceny.nazwa_kategorii
            else:
                nazwa_kategorii = "Inne"

            podsumowanie[nazwa_kategorii] += float(szczegol.cena_calkowita) or 0.0

        return dict(podsumowanie)

    @property
    def dane_handlowca(self):
        if self.handlowiec:
            return {"imie": self.handlowiec.user.imie, "nazwisko": self.handlowiec.user.nazwisko, "email": self.handlowiec.email, "nr_kontaktowy": self.handlowiec.nr_kontaktowy}
        return "Brak przypisanego handlowca"

    def wyslano_wycene(self):
        self.data_wyslania = dt.now()
        self.status_wyceny = self.opcje_statusu[2]
    
    def zamknij_wycene(self, zaakceptowano=True, powod_odrzucenia:str=None):
        self.data_zamkniecia = dt.now()
        if zaakceptowano:
            self.status_wyceny = self.opcje_statusu[3]
        else:
            self.status_wyceny = self.opcje_statusu[4]
            self.powod_odrzucenia = powod_odrzucenia

    def aktualizuj_z_formularza(self, form):
        """
        funkcja aktualizujaca dane wyceny
        """
        self.imie_klienta = form.get("imie_klienta")
        self.nazwisko_klienta = form.get("nazwisko_klienta")
        self.numer_domu = form.get("numer_domu")
        self.ulica = form.get("ulica")
        self.miasto = form.get("miasto")
        self.kod_pocztowy = form.get("kod_pocztowy")
        self.kontakt_telefon = form.get("kontakt_telefon")
        self.kontakt_email = form.get("kontakt_email")
        self.dodatkowe_uwagi = form.get("dodatkowe_uwagi")

class Szczegoly_Wyceny(Base):
    __tablename__ = "szczegoly_wyceny"

    szwycid = Column(Integer, primary_key=True)
    wycid = Column(Integer, ForeignKey("wycena.wycid"), nullable=False)
    pozid = Column(Integer, ForeignKey("pozycje_wyceny.cid"), nullable=True)
    ilosc = Column(Numeric(10,4), default=0.0)
    cena_calkowita = Column(Numeric(10,2), default=0.0) #pozycje_wyceny.cena_jednostkowa x ilosc lub możliwosc wpisania z palca
    indywidualna_nazwa = Column(String(128), default=None) #dodawany w wyjatkowych sytuacjach gdy wiersz nie jest powiązany z pozycje wyceny
    dodatkowy_opis = Column(String(256))
    data_wprowadzenia = Column(DateTime, default=dt.now)
    data_edycji = Column(DateTime, default=dt.now, onupdate=dt.now)

    wycena = relationship("Wycena", back_populates="szczegoly", lazy="joined")
    pozycja = relationship("Pozycje_Wyceny", backref="szczegoly", lazy="joined")

    def __init__(self, form, wycid, session):
        self.wycid = wycid
        self.pozid = form.get("pozid")  # może być None
        self.ilosc = float(form.get("ilosc", 0)) or float(0)
        if form.get("indywidualna_nazwa"):
            self.indywidualna_nazwa = form.get("wybrana_wartosc") or None
        self.dodatkowy_opis = form.get("dodatkowy_opis")

        # Jeśli powiązana pozycja istnieje – pobierz cenę jednostkową
        if self.pozid:
            pozycja = session.query(Pozycje_Wyceny).filter_by(cid=self.pozid).first()
            if pozycja:
                self.cena_calkowita = round(self.ilosc * float(pozycja.cena_jednostkowa), 2)
            else:
                self.cena_calkowita = float(0)
        else:
            
            self.cena_calkowita = float(0)


class Oferta(Base):
    __tablename__ = "oferta"

    zamid = Column(Integer, primary_key=True)
    rok = Column(Integer)
    kolejny_numer = Column(Integer)
    nr_zlecenia = Column(String(64), nullable=False, unique=True)
    imie_klienta = Column(String(128), nullable=False)
    nazwisko_klienta = Column(String(128), nullable=False)
    data_zlecenia = Column(Date, nullable=False)
    data_wprowadzenia = Column(Date, default=dt.now)
    termin_realizacji = Column(Date, nullable=True)
    adres = Column(String(256))
    ulica = Column(String(256))
    miasto = Column(String(256))
    kod_pocztowy = Column(String(16))
    kontakt_telefon = Column(String(64))
    kontakt_email = Column(String(128))
    dane_faktura = Column(String)

    typ_klienta = Column(Boolean) # 0 - os. fiz, 1 - firma
    status_zlecenia = Column(String, default="Wprowadzone") #Wprowadzone, Wysłane, Odrzucone, Opłacone, Realizacja, Zakończone
    data_wyslania = Column(Date, nullable=True)
    powod_odrzucenia = Column(String)
    dodatkowe_uwagi = Column(String)


    szczegoly = relationship("Oferta_Szczegoly", back_populates="oferta", cascade="all, delete-orphan")


    def __init__(self, nr_zlecenia: str, imie_nazwisko: str, data_zlecenia, termin_realizacji, adres_inwestycji: str, kontakt_telefon: str,
        kontakt_email: str, dane_faktura: str, typ_klienta: bool):

        self.nr_zlecenia = nr_zlecenia
        self.imie_nazwisko = imie_nazwisko
        self.data_zlecenia = data_zlecenia
        self.termin_realizacji = termin_realizacji
        self.adres_inwestycji = adres_inwestycji
        self.kontakt_telefon = kontakt_telefon
        self.kontakt_email = kontakt_email
        self.dane_faktura = dane_faktura
        self.typ_klienta = typ_klienta
        

    @classmethod
    def from_form(cls, form):

        def get_date(field):
            val = form.get(field)
            return dt.strptime(val, '%Y-%m-%d').date() if val else None

        return cls(
            nr_zlecenia=form.get("nr_zlecenia"),
            imie_nazwisko=form.get("imie_nazwisko"),
            data_zlecenia=get_date("data_zlecenia"),
            termin_realizacji=get_date("termin_realizacji"),
            adres_inwestycji=form.get("adres_inwestycji"),
            kontakt_telefon=form.get("kontakt_telefon"),
            kontakt_email=form.get("kontakt_email"),
            dane_faktura=form.get("dane_faktura"),
            typ_klienta=True if form.get("typ_klienta") == "firma" else False            
        )
    
    def to_dict(self):
        return {
            "zamid": self.zamid,
            "nr_zlecenia": self.nr_zlecenia,
            "imie_nazwisko": self.imie_nazwisko,
            "data_zlecenia": self.data_zlecenia.strftime("%Y-%m-%d") if self.data_zlecenia else "", # type: ignore
            "data_wprowadzenia": self.data_wprowadzenia.strftime("%Y-%m-%d") if self.data_wprowadzenia else "", # type: ignore
            "termin_realizacji": self.termin_realizacji.strftime("%Y-%m-%d") if self.termin_realizacji else "", # type: ignore
            "adres_inwestycji": self.adres_inwestycji,
            "kontakt_telefon": self.kontakt_telefon,
            "kontakt_email": self.kontakt_email
        }
    
class Oferta_Szczegoly(Base):
    __tablename__ = "oferta_szczegoly"

    ofsid = Column(Integer, primary_key=True)
    oferta_id = Column(Integer, ForeignKey('oferta.zamid'), nullable=False)
    sekcja = Column(String(128), nullable=False)
    opis = Column(String)
    ilosc = Column(String(16))
    cena = Column(Float)
    data_utworzenia = Column(Date, default=dt.now)
    data_edycji =  Column(DateTime, default=dt.now, onupdate=dt.now)

    oferta = relationship("Oferta", back_populates="szczegoly")

    def __init__(self, oferta_id, sekcja, opis, ilosc, cena):
        self.oferta_id = int(oferta_id)
        self.sekcja = sekcja
        self.opis = opis
        self.ilosc = ilosc
        try:
            self.cena = float(str(cena).replace("zł", "").strip())
        except (ValueError, TypeError):
            self.cena = None  # albo 0.0, jeśli chcesz domyślnie

    @classmethod
    def from_dict(cls, data: dict, oferta_id: int):
        return cls(
            oferta_id=oferta_id,
            sekcja=data.get("sekcja"),
            opis=data.get("opis"),
            ilosc=data.get("ilosc"),
            cena=data.get("cena")
        )