from flask import Blueprint, jsonify
from models import db, CatalogItem, CatalogGroup, CatalogCategory, PriceKind

catalog_bp = Blueprint("catalog", __name__, url_prefix="/api/catalog")

# @catalog_bp.get("/items")
# def api_items():
#     # zwracamy płaską listę z "ścieżką" do wyświetlania
#     q = (
#         db.session.query(CatalogItem, CatalogGroup, CatalogCategory)
#         .join(CatalogGroup, CatalogItem.group_id == CatalogGroup.id)
#         .join(CatalogCategory, CatalogGroup.category_id == CatalogCategory.id)
#         .filter(CatalogItem.is_active.is_(True))
#         .order_by(CatalogCategory.name, CatalogGroup.name, CatalogItem.name)
#     )

#     items = []
#     for item, grp, cat in q.all():
#         items.append({
#             "id": item.id,
#             "path_title": f"{cat.name} / {grp.name} / {item.name}",
#             "unit": item.unit.value if item.unit else None,
#             "price_kind": item.price_kind.value,
#             "price_value": float(item.price_value) if item.price_value is not None else None,
#             "price_formula": item.price_formula,
#         })

#     return jsonify({"items": items})

@catalog_bp.get("/items")
def api_items():
    q = (
        db.session.query(CatalogItem, CatalogGroup, CatalogCategory)
        .join(CatalogGroup, CatalogItem.group_id == CatalogGroup.id)
        .join(CatalogCategory, CatalogGroup.category_id == CatalogCategory.id)
        .filter(CatalogItem.is_active.is_(True))
        .order_by(CatalogCategory.name, CatalogGroup.name, CatalogItem.name)
    )

    items = []
    for item, grp, cat in q.all():
        items.append({
            "id": item.id,
            "category_name": cat.name,      # Grupa I
            "group_name": grp.name,         # Grupa II
            "item_name": item.name,         # Grupa III
            "path_title": f"{cat.name} / {grp.name} / {item.name}",
            "unit": item.unit.value if item.unit else None,
            "price_kind": item.price_kind.value,
            "price_value": float(item.price_value) if item.price_value is not None else None,
            "price_formula": item.price_formula,
        })

    return jsonify({"items": items})
