"""
One-time data migration: PostgreSQL -> DuckDB
"""

import os
import sys

from sqlalchemy import create_engine, text

from app import app, db
from models.activation import Activation
from models.expedition_plan import ExpeditionPlan
from models.media import MediaFile
from models.object import YLFFObject
from models.page_content import PageContent
from models.qso_record import QSORecord
from models.user import User

PG_URL = os.getenv("PG_DATABASE_URL") or os.getenv("DATABASE_URL")

if not PG_URL:
    sys.exit("Set PG_DATABASE_URL or DATABASE_URL first")

TABLES_IN_ORDER = [
    (User, "users"),
    (YLFFObject, "ylff_objects"),
    (PageContent, "page_contents"),
    (Activation, "activations"),
    (QSORecord, "qso_records"),
    (MediaFile, "media_files"),
    (ExpeditionPlan, "expedition_plans"),
]


def main():
    source_engine = create_engine(PG_URL)

    with app.app_context(), source_engine.connect() as pg_conn:
        for model, table_name in reversed(TABLES_IN_ORDER):
            db.session.execute(model.__table__.delete())
            db.session.commit()
            print(f"{table_name}: cleared DuckDB destination")

        for model, table_name in TABLES_IN_ORDER:
            result = pg_conn.execute(text(f"SELECT * FROM {table_name}"))
            rows = [dict(row) for row in result.mappings().all()]

            if not rows:
                print(f"{table_name}: 0 rows in Postgres, skipping")
                continue

            db.session.execute(model.__table__.insert(), rows)
            db.session.commit()

            print(f"{table_name}: migrated {len(rows)} rows")

            if "id" in rows[0]:
                max_id = max(row["id"] for row in rows)
                _fix_sequence(table_name, max_id)

    print("\nDONE. DuckDB file:", app.config["SQLALCHEMY_DATABASE_URI"])


def _fix_sequence(table_name, max_id):
    seq_name = f"{table_name}_id_seq"
    try:
        db.session.execute(text(f"ALTER SEQUENCE {seq_name} RESTART WITH {max_id + 1}"))
        db.session.commit()
        print(f"  -> sequence {seq_name} restarted at {max_id + 1}")
    except Exception as error:
        db.session.rollback()
        print(f"  -> could not adjust sequence {seq_name}: {error}")


if __name__ == "__main__":
    main()
