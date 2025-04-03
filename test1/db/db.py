from functools import wraps

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

SERVER = "localhost"
DATDBASE = "api_data"
DRIVER = "ODBC Driver 17 for SQL Server"
connection_string = f"mssql+pyodbc://@{SERVER}/{DATDBASE}?driver={DRIVER}&TrustServerCertificate=yes"

def with_db_session(session: sessionmaker):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            db: Session = session()
            try:
                kwargs['session'] = db
                result = func(*args, **kwargs)
                db.commit()
                return result
            except Exception as e:
                db.rollback()
                raise e
            finally:
                db.close()
                print("Session closed")
        return wrapper
    return decorator

def get_engine(connection_string=connection_string):
    try:
        engine = create_engine(connection_string, isolation_level="AUTOCOMMIT", echo=False)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print(DATDBASE, 'engine')
        return engine
    except:
        connection_string = f"mssql+pyodbc://@{SERVER}/master?driver={DRIVER}&TrustServerCertificate=yes"
        engine = create_engine(connection_string, isolation_level="AUTOCOMMIT", echo=True)
        with engine.connect() as conn:
            conn.execute(text(f"CREATE DATABASE {DATDBASE}"))
        print('CREATE DATABASE api_data')
        return get_engine()

engine = get_engine(connection_string)
SessionLocal = sessionmaker(bind=engine)

if __name__ == '__main__':
    with engine.connect() as conn:
        result = conn.execute(text("SELECT @@VERSION"))
        print(result.fetchone())

