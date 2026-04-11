from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

DATABASE_URL = "sqlite:///./shipments.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def execute_with_sql(db: Session, stmt, mapping: bool = False, first: bool = False):
    if mapping:
        result = [dict(row._mapping) for row in db.execute(stmt).all()]
    elif first:
        result = db.execute(stmt).scalars().first()
    else:
        result = db.execute(stmt).scalars().all()
    
    return {
        "sql": str(stmt),
        "data": result
    }