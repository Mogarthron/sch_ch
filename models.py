from sqlalchemy import Column, Integer, Numeric, Float, String, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime as dt

Base = declarative_base()

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

class Pozycje_Wyceny(Base):
    __tablename__ = "pozycje_wyceny"

    cid = Column(Integer, primary_key=True)
    kategoria_id = Column(Integer, ForeignKey('kategorie_wyceny.katid'), nullable=False)
    pozycja = Column(String(128), nullable=False)
    cena_jednostkowa = Column(Numeric(10,2))
    jednostka_miary = Column(String(16))
    data_wprowadzenia = Column(DateTime, default=dt.now)
    data_edycji = Column(DateTime, default=dt.now, onupdate=dt.now)

    # kategoria_wyceny = relationship("Kategorie_Wyceny", back_populates="kategorie_wyceny")
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