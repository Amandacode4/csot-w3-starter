"""CSOT Week 3 starter app — Flask + SQLite.

Two endpoints are pre-wired. Add your own routes below.
Grader requires BOTH:
  GET /health       → {"status": "ok"}
  GET /api/version  → {"version": "<VERSION file content>"}
"""
from __future__ import annotations

import os
from pathlib import Path

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# VERSION file lives at the repo root (one level above app/)
ROOT = Path(__file__).resolve().parents[1]
VERSION_FILE = ROOT / "VERSION"

app = Flask(__name__)

db_url = os.environ.get("DATABASE_URL", f"sqlite:///{ROOT / 'instance' / 'app.db'}")
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Item(db.Model):
    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)


def _version() -> str:
    return VERSION_FILE.read_text(encoding="utf-8").strip() if VERSION_FILE.is_file() else "0.0.0"


# ── Required by grader — do not remove ───────────────────────────────────────

@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/api/version")
def version():
    return jsonify({"version": _version()})


# ── Add your routes below ─────────────────────────────────────────────────────

@app.get("/api/items")
def list_items():
    rows = Item.query.order_by(Item.id).all()
    return jsonify({"items": [{"id": r.id, "name": r.name} for r in rows]})


@app.post("/api/items")
def create_item():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    if not name:
        return jsonify({"error": "name required"}), 400
    row = Item(name=name)
    db.session.add(row)
    db.session.commit()
    return jsonify({"id": row.id, "name": row.name}), 201


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
