"""Create all database tables from SQLAlchemy models (dev bootstrap).

Prefer Alembic migrations in production:
  alembic revision --autogenerate -m "initial"
  alembic upgrade head
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.db.base import Base
from app.db.session import engine
import app.db.base_models  # noqa: F401


def main() -> None:
    print(f"Connecting to: {engine.url}")
    Base.metadata.create_all(bind=engine)
    print("All tables created.")


if __name__ == "__main__":
    main()
