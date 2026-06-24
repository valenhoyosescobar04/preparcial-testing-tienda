import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer
from src.database.models import Base


@pytest.fixture(scope="session")
def postgres_container():
    """Levanta un contenedor PostgreSQL real para toda la sesión de pruebas."""
    with PostgresContainer("postgres:16-alpine") as postgres:
        yield postgres


@pytest.fixture(scope="session")
def engine(postgres_container):
    """Crea el engine SQLAlchemy apuntando al contenedor de pruebas."""
    db_url = postgres_container.get_connection_url()
    _engine = create_engine(db_url)
    Base.metadata.create_all(bind=_engine)
    yield _engine
    _engine.dispose()


@pytest.fixture(scope="function")
def db_session(engine):
    """
    Fixture con patrón ROLLBACK:
    - Abre una conexión y una transacción externa.
    - Cada prueba trabaja dentro de esa transacción.
    - Al finalizar (pase o falle), hace ROLLBACK → BD queda limpia.
    """
    connection = engine.connect()
    transaction = connection.begin()

    SessionTest = sessionmaker(bind=connection)
    session = SessionTest()

    yield session

    session.close()
    transaction.rollback()
    connection.close()