from src.models import db
from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(bind=db, autocommit=False, autoflush=False)


def get_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()
