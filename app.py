from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, Quote, QuoteItem, CatalogItem
from blueprints.catalog import catalog_bp

import json
from decimal import Decimal

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = "dev"

    db.init_app(app)
    app.register_blueprint(catalog_bp)

    @app.get("/")
    def index():
        return redirect(url_for("form"))

    @app.get("/form")
    def form():
        return render_template("wycena_form.html")

    @app.post("/quotes")
    def create_quote():
        # zapis wyceny + pozycji z JSON-a z formularza
        items_json = request.form.get("items_json") or "[]"
        items = json.loads(items_json)

        q = Quote(
            customer_name=request.form.get("customer_name") or "—",
            customer_phone=request.form.get("customer_phone"),
            customer_email=request.form.get("customer_email"),
            order_no=request.form.get("order_no"),
        )
        db.session.add(q)
        db.session.flush()

        total = Decimal("0.00")
        for it in items:
            unit_price = it.get("unit_price")
            qty = Decimal(str(it.get("qty", 0) or 0))
            price_kind = it.get("price_kind", "manual")

            line_total = None
            if price_kind == "fixed" and unit_price is not None:
                up = Decimal(str(unit_price))
                line_total = (up * qty).quantize(Decimal("0.01"))
                total += line_total

            qi = QuoteItem(
                quote_id=q.id,
                catalog_item_id=it.get("catalog_item_id"),
                title_snapshot=it.get("title") or "—",
                unit_snapshot=it.get("unit"),
                qty=qty,
                price_kind_snapshot=price_kind,
                unit_price_snapshot=Decimal(str(unit_price)).quantize(Decimal("0.01")) if unit_price is not None else None,
                line_total=line_total,
            )
            db.session.add(qi)

        q.total_net = total
        q.total_gross = total
        db.session.commit()

        return redirect(url_for("form"))

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
