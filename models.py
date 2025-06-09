from sqlalchemy import Column, Integer, Float, String, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime as dt

Base = declarative_base()

class Oferta(Base):
    __tablename__ = 'oferta'

    zamid = Column(Integer, primary_key=True)
    nr_zlecenia = Column(String(64), nullable=False, unique=True)
    imie_nazwisko = Column(String(128), nullable=False)
    data_zlecenia = Column(Date, nullable=False)
    data_wprowadzenia = Column(Date, default=dt.now)
    termin_realizacji = Column(Date, nullable=True)
    adres_inwestycji = Column(String(255))
    kontakt_telefon = Column(String(64))
    kontakt_email = Column(String(128))
    dane_faktura = Column(String)

    typ_klienta = Column(Boolean) # 0 - os. fiz, 1 - firma
    typ_schodow = Column(String(128))
    material = Column(String(128))
    wykonczenie_schodow = Column(String(128))
    kolor_wykonczenia_schodow = Column(String(128))
    typ_balustrady = Column(String(128))
    obrobka_stropu = Column(String(128))
    polaczenie_z_posadzka = Column(String(128))
    status_zlecenia = Column(String, default="Wprowadzone") #Wprowadzone, Wysłane, Odrzucone, Opłacone, Realizacja, Zakończone
    data_wyslania = Column(Date, nullable=True)
    powod_odrzucenia = Column(String)
    dodatkowe_uwagi = Column(String)


    szczegoly = relationship("Oferta_Szczegoly", back_populates="oferta", cascade="all, delete-orphan")


    def __init__(self, nr_zlecenia: str, imie_nazwisko: str, data_zlecenia, termin_realizacji, adres_inwestycji: str, kontakt_telefon: str,
        kontakt_email: str, dane_faktura: str, typ_klienta: bool, typ_schodow: str, material: str, wykonczenie_schodow: str,
        kolor_wykonczenia_schodow: str, typ_balustrady: str, obrobka_stropu: str, polaczenie_z_posadzka: str):

        self.nr_zlecenia = nr_zlecenia
        self.imie_nazwisko = imie_nazwisko
        self.data_zlecenia = data_zlecenia
        self.termin_realizacji = termin_realizacji
        self.adres_inwestycji = adres_inwestycji
        self.kontakt_telefon = kontakt_telefon
        self.kontakt_email = kontakt_email
        self.dane_faktura = dane_faktura
        self.typ_klienta = typ_klienta
        self.typ_schodow = typ_schodow
        self.material = material
        self.wykonczenie_schodow = wykonczenie_schodow
        self.kolor_wykonczenia_schodow = kolor_wykonczenia_schodow
        self.typ_balustrady = typ_balustrady
        self.obrobka_stropu = obrobka_stropu
        self.polaczenie_z_posadzka = polaczenie_z_posadzka

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
            typ_klienta=True if form.get("typ_klienta") == "firma" else False,
            typ_schodow=form.get("typy_schodow"),
            material=form.get("material"),
            wykonczenie_schodow=form.get("wykonczenie_schodow"),
            kolor_wykonczenia_schodow=form.get("kolor_wykonczenia_schodow"),
            typ_balustrady=form.get("typ_balustrady"),
            obrobka_stropu=form.get("obrobka_stropu"),
            polaczenie_z_posadzka=form.get("polaczenie_z_posadzka")
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
            "kontakt_email": self.kontakt_email,
            "typy_schodow": self.typ_schodow,
            "material": self.material,
            "wykonczenie_schodow": self.wykonczenie_schodow,
            "kolor_wykonczenia_schodow": self.kolor_wykonczenia_schodow,
            "typ_balustrady": self.typ_balustrady,
            "obrobka_stropu": self.obrobka_stropu,
            "polaczenie_z_posadzka": self.polaczenie_z_posadzka,
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