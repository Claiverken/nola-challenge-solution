# database.py
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL não foi definida no ficheiro .env")


engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_connection():
    try:
        # Tenta ligar e executar uma query super simples
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            print("Conexão com a base de dados bem-sucedida!")
            return True
    except OperationalError as e:
        print(f"Erro ao conectar à base de dados: {e}")
        return False