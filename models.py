from __future__ import annotations

import enum
from datetime import datetime
from decimal import Decimal

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class UnitEnum(str, enum.Enum):
    mb = "mb"
    szt = "szt"
    m2 = "m2"
    kpl = "kpl"
    kompl = "kompl"
import enum
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class StairKind(str, enum.Enum):
    GRZEBIENIOWE = "grzebieniowe"
    POLICZKOWE = "policzkowe"
    KONSTR_METALOWA = "konstr_metalowa"
    DYWANOWE = "dywanowe"
    WSPORNIKOWE = "wspornikowe"


class GrzebienioweType(str, enum.Enum):
    PELNE = "pelne"
    AZUROWE = "azurowe"
    Z_ZABUDOWA = "z_zabudowa"


class PoliczkoweType(str, enum.Enum):
    PELNE = "pelne"
    AZUROWE = "azurowe"
    BOLCOWE = "bolcowe"


class MetalStairType(str, enum.Enum):
    TYP_I = "TYP_I"     # proste na dwóch profilach stalowych
    TYP_II = "TYP_II"   # zabiegowe i proste, stopnie nakładane na konstrukcję
    TYP_III = "TYP_III" # zabiegowe i proste, stopnie wchodzą pomiędzy policzki metalowe
    TYP_IV = "TYP_IV"   # zabiegowe i proste, dywanowe na konstrukcji metalowej
    TYP_V = "TYP_V"     # proste na 1 profilu stalowym


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Quote(db.Model, TimestampMixin):
    __tablename__ = "quote"
    id: Mapped[int] = mapped_column(primary_key=True)

    customer_name: Mapped[str] = mapped_column(db.String(180), nullable=False)

    stairs: Mapped["StairsConfig"] = relationship(
        back_populates="quote", uselist=False, cascade="all, delete-orphan"
    )

    items = db.relationship(
        "QuoteItem",
        back_populates="quote",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class StairsConfig(db.Model, TimestampMixin):
    """
    Dokładnie jedna konfiguracja schodów na jedną wycenę.
    """
    __tablename__ = "stairs_config"
    id: Mapped[int] = mapped_column(primary_key=True)
    quote_id: Mapped[int] = mapped_column(db.ForeignKey("quote.id"), unique=True, nullable=False)

    kind: Mapped[StairKind] = mapped_column(db.Enum(StairKind), nullable=False)

    # podtypy zależne od kind:
    grzebieniowe_type: Mapped[GrzebienioweType | None] = mapped_column(db.Enum(GrzebienioweType), nullable=True)
    policzkowe_type: Mapped[PoliczkoweType | None] = mapped_column(db.Enum(PoliczkoweType), nullable=True)
    metal_type: Mapped[MetalStairType | None] = mapped_column(db.Enum(MetalStairType), nullable=True)

    extra_notes: Mapped[str | None] = mapped_column(db.Text)

    quote: Mapped["Quote"] = relationship(back_populates="stairs")

    def validate(self) -> None:
        """
        Wymusza spójność:
        - GRZEBIENIOWE -> grzebieniowe_type wymagane, reszta None
        - POLICZKOWE   -> policzkowe_type wymagane, reszta None
        - METALOWA     -> metal_type wymagane, reszta None
        - DYWANOWE/WSPORNIKOWE -> wszystkie podtypy None
        """
        if self.kind == StairKind.GRZEBIENIOWE:
            if self.grzebieniowe_type is None:
                raise ValueError("Dla GRZEBIENIOWE wymagany jest podtyp.")
            self.policzkowe_type = None
            self.metal_type = None

        elif self.kind == StairKind.POLICZKOWE:
            if self.policzkowe_type is None:
                raise ValueError("Dla POLICZKOWE wymagany jest podtyp.")
            self.grzebieniowe_type = None
            self.metal_type = None

        elif self.kind == StairKind.KONSTR_METALOWA:
            if self.metal_type is None:
                raise ValueError("Dla KONSTRUKCJI METALOWEJ wymagany jest typ I–V.")
            self.grzebieniowe_type = None
            self.policzkowe_type = None

        elif self.kind in (StairKind.DYWANOWE, StairKind.WSPORNIKOWE):
            self.grzebieniowe_type = None
            self.policzkowe_type = None
            self.metal_type = None
        else:
            raise ValueError("Nieznany rodzaj schodów.")


class PriceKind(str, enum.Enum):
    fixed = "fixed"     # liczba
    formula = "formula" # string zaczyna się od "="
    manual = "manual"   # brak ceny / do ręcznego ustalenia


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class CatalogCategory(db.Model, TimestampMixin):
    __tablename__ = "catalog_category"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(120), unique=True, nullable=False)

    groups: Mapped[list["CatalogGroup"]] = relationship(back_populates="category", cascade="all, delete-orphan")


class CatalogGroup(db.Model, TimestampMixin):
    """
    Grupa II (podkategoria) w obrębie Grupa I
    """
    __tablename__ = "catalog_group"
    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(db.ForeignKey("catalog_category.id"), nullable=False)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)

    category: Mapped["CatalogCategory"] = relationship(back_populates="groups")
    items: Mapped[list["CatalogItem"]] = relationship(back_populates="group", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("category_id", "name", name="uq_catalog_group_category_name"),
    )


class CatalogItem(db.Model, TimestampMixin):
    """
    Grupa III + cena/jednostka
    """
    __tablename__ = "catalog_item"
    id: Mapped[int] = mapped_column(primary_key=True)
    group_id: Mapped[int] = mapped_column(db.ForeignKey("catalog_group.id"), nullable=False)

    name: Mapped[str] = mapped_column(db.String(255), nullable=False)          # Grupa III
    unit: Mapped[UnitEnum | None] = mapped_column(db.Enum(UnitEnum), nullable=True)

    price_kind: Mapped[PriceKind] = mapped_column(db.Enum(PriceKind), default=PriceKind.manual, nullable=False)
    price_value: Mapped[Decimal | None] = mapped_column(db.Numeric(12, 2), nullable=True)  # gdy fixed
    price_formula: Mapped[str | None] = mapped_column(db.String(255), nullable=True)       # gdy formula

    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    group: Mapped["CatalogGroup"] = relationship(back_populates="items")

    __table_args__ = (
        UniqueConstraint("group_id", "name", name="uq_catalog_item_group_name"),
    )



class QuoteItem(db.Model, TimestampMixin):
    __tablename__ = "quote_item"
    id: Mapped[int] = mapped_column(primary_key=True)
    quote_id: Mapped[int] = mapped_column(db.ForeignKey("quote.id"), nullable=False)
    catalog_item_id: Mapped[int | None] = mapped_column(db.ForeignKey("catalog_item.id"), nullable=True)

    title_snapshot: Mapped[str] = mapped_column(db.String(512), nullable=False)  # "Grupa I / Grupa II / Grupa III"
    unit_snapshot: Mapped[str | None] = mapped_column(db.String(10))
    qty: Mapped[Decimal] = mapped_column(db.Numeric(12, 3), default=Decimal("1.0"), nullable=False)

    price_kind_snapshot: Mapped[str] = mapped_column(db.String(20), nullable=False)  # fixed/formula/manual
    unit_price_snapshot: Mapped[Decimal | None] = mapped_column(db.Numeric(12, 2))
    line_total: Mapped[Decimal | None] = mapped_column(db.Numeric(12, 2))

    quote: Mapped["Quote"] = relationship(back_populates="items")
    catalog_item: Mapped["CatalogItem"] = relationship()
