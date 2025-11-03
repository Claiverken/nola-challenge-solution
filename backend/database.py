# database.py
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv

# 1. Carrega as variáveis do ficheiro .env que acabámos de criar
load_dotenv()

# 2. Lê a string de conexão do .env
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL não foi definida no ficheiro .env")

# 3. Cria o "motor" (engine) do SQLAlchemy para a ligação
engine = create_engine(DATABASE_URL)

# 4. Cria uma "fábrica" de sessões (é o que usamos para fazer queries)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. Função de dependência para o FastAPI
# Esta é a forma correta de garantir que abrimos e fechamos
# uma ligação à base de dados em cada pedido à API.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 6. Função para testar a conexão
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