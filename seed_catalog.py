from decimal import Decimal
import openpyxl

from models import db, CatalogCategory, CatalogGroup, CatalogItem, PriceKind, UnitEnum

def seed_catalog_from_xlsx(xlsx_path: str) -> None:
    wb = openpyxl.load_workbook(xlsx_path, data_only=True)
    ws = wb.active  # Arkusz1

    # headers: Grupa I, Grupa II, Grupa III, Cena, jedn
    first = True
    for row in ws.iter_rows(values_only=True):
        if first:
            first = False
            continue

        g1, g2, g3, cena, jedn = row
        if not (g1 and g2 and g3):
            continue

        # 1) category
        cat = db.session.query(CatalogCategory).filter_by(name=str(g1).strip()).one_or_none()
        if not cat:
            cat = CatalogCategory(name=str(g1).strip())
            db.session.add(cat)
            db.session.flush()

        # 2) group
        grp = (
            db.session.query(CatalogGroup)
            .filter_by(category_id=cat.id, name=str(g2).strip())
            .one_or_none()
        )
        if not grp:
            grp = CatalogGroup(category_id=cat.id, name=str(g2).strip())
            db.session.add(grp)
            db.session.flush()

        # 3) item
        item = (
            db.session.query(CatalogItem)
            .filter_by(group_id=grp.id, name=str(g3).strip())
            .one_or_none()
        )
        if not item:
            item = CatalogItem(group_id=grp.id, name=str(g3).strip())
            db.session.add(item)

        # unit
        unit = str(jedn).strip() if jedn else None
        item.unit = UnitEnum(unit) if unit in UnitEnum._value2member_map_ else None

        # price
        item.price_value = None
        item.price_formula = None
        if cena is None or str(cena).strip() == "":
            item.price_kind = PriceKind.manual
        else:
            # Excel potrafi zwrócić formułę jako string (gdy plik nie ma zapisanych wyników obliczeń)
            if isinstance(cena, str) and cena.strip().startswith("="):
                item.price_kind = PriceKind.formula
                item.price_formula = cena.strip()
            else:
                # liczba
                try:
                    item.price_kind = PriceKind.fixed
                    item.price_value = Decimal(str(cena)).quantize(Decimal("0.01"))
                except Exception:
                    item.price_kind = PriceKind.manual

        item.is_active = True

    db.session.commit()


if __name__ == "__main__":
    from app import app
    from models import db

    with app.app_context():
        db.create_all()
        seed_catalog_from_xlsx("Dane do wycen.xlsx")

    print("Cennik zaimportowany.")
