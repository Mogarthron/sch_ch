from sqlalchemy import Column, Integer, Numeric, Float, String, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime as dt
from sqlalchemy import func, cast, Float, Integer
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_login import UserMixin

from collections import defaultdict

Base = declarative_base()

class Grupy_produktowe(Base):
    """
    Grupy opisujące katagorie pozycji w bazie danych
    """
    __tablename__ = "grupy_produktowe"

    grupa_id = Column(Integer, primary_key=True)
    nazawa_grupy = Column(String(128), nullable=False) #Schody, Balustrady, Dopłaty, ..., Schody policzkowe
    skrot_grupy = Column(String(8), nullable=False) #np. sch, bal, schPo 
    opis_gropy = Column(String(256), nullable=False)

class Jednostki(Base):
    __tablename__ = "jednostki"

    jedn_id = Column(Integer, primary_key=True)
    nazwa_jednostki = Column(String(128), nullable=False)
    skrot_nazwy = Column(String(8), nullable=False)

class Pozycja(Base):
    __tablename__ = "pozycja"

    pozycja_id = Column(Integer, primary_key=True)
    nazwa_pozycji = Column(String(256), nullable=False)
    zdjecie1_url = Column(String, nullable=True)
    zdjecie2_url = Column(String, nullable=True)
    zdjecie3_url = Column(String, nullable=True)
    model1_url = Column(String, nullable=True)
    jednosta_id = Column(Integer, ForeignKey("jednostki.jedn_id", ondelete="SET NULL"), nullable=False)
    jednosta_pomocnicza_id = Column(Integer, ForeignKey("jednostki.jedn_id", ondelete="SET NULL"), nullable=True)
    przelicznik_jdn_jdnpomoc = Column(Float, nullable=True)

class Poz_grop(Base):
    __tablename__ = "poz_grop"

    poz_grop_id = Column(Integer, primary_key=True)
    poz_id = Column(Integer, ForeignKey("pozycja.pozycja_id", "CASCADE"))
    gro_id = Column(Integer, ForeignKey("grupy_produktowe.grupa_id", "CASCADE"))
    hierarchia = Column(Integer, default=1) #im wyższa tym ważniejsza dobrze numerować pokolei dla jednej pozycji
    

class Klient(Base): 
    __tablename__ = "klient"

    klient_id = Column(Integer, primary_key=True)
    klient_nazwa = Column(String(256), nullable=False)
    klient_kod = Column(String(64), nullable=True)
    kupujacy = Column(Boolean) #czy to klient od którego kupujemy czy ktróemu sprzedajemy
    adres = Column(String(64), nullable=True)
    tel_kontaktowy = Column(String(64), nullable=True)
    mail_kontaktowy = Column(String(64), nullable=True)

class Pozycje_sprzedarzowe(Base):
    __tablename__ = "pozycje_sprzedarzowe"

    poz_sprzedaz_id = Column(Integer, primary_key=True)
    poz_id = Column(Integer, ForeignKey("pozycja.pozycja_id"))
    nazwa_handlowa = Column(String(256), nullable=False)
    klient_id = Column(Integer, ForeignKey("pozycja.pozycja_id"), nullable=False) #pozycja może być utworzona dla klientów indywidualnych
    cena_sprzedarzowa = Column(Numeric(10,4), default=1)

class Zamowienie_klienta(Base):
    __tablename__ = "zamowienie_klienta"

    zam_klienta_id = Column(Integer, primary_key=True)
    zam_jednorazowe = Column(Boolean, default=True) #precyzuje czy zamóienie do tego klienta będzie się powtarzac czy nie
    klient_id = Column(Integer, ForeignKey("klient.klient_id"), nullable=True)

    nazwa_klienta = Column(String(256))
    kraj_klienta = Column(String(128))
    kodpocztowy_klienta = Column(String(32))
    miasto_klienta = Column(String(128))
    ulica_klienta = Column(String(256))
    numerdomu_klienta = Column(String(64))
    
    telefon_klienta = Column(String(64))
    email_klienta = Column(String(64))
    
    email_klienta = Column(String(64))
    

    

