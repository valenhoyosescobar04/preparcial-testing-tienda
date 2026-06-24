import pytest
from fastapi.testclient import TestClient
from src.carrito.api import app
from src.database.config import get_db


def test_post_producto_respuesta_correcta_y_persiste_en_db(db_session):
    """
    Realiza POST al endpoint con override de dependencia,
    valida respuesta HTTP 201 y que el dato existe en PostgreSQL.
    """
    # Override: reemplaza get_db con la sesión de TestContainers
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)

    payload = {
        "nombre": "Laptop Gamer",
        "precio": 3500000.0,
        "cantidad": 1
    }

    response = client.post("/carrito/sesion-api-test-001/productos", json=payload)

    # Validar respuesta HTTP
    assert response.status_code == 201
    data = response.json()
    assert data["mensaje"] == "Producto agregado"
    assert "item_id" in data
    assert isinstance(data["item_id"], int)

    # Validar que persiste en la BD
    from src.database.models import ItemCarritoDB
    item_en_db = db_session.query(ItemCarritoDB).filter(
        ItemCarritoDB.id == data["item_id"]
    ).first()

    assert item_en_db is not None
    assert item_en_db.nombre == "Laptop Gamer"
    assert item_en_db.precio == 3500000.0

    app.dependency_overrides.clear()


def test_get_carrito_retorna_total_correcto(db_session):
    """
    Agrega productos via repositorio y verifica que GET /carrito
    retorna el total correcto.
    """
    from src.database.repositorio import CarritoRepositorio

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    sesion_id = "sesion-get-test-002"
    repo = CarritoRepositorio(db_session)
    repo.agregar_item(sesion_id, "Monitor", 900000.0, 2)

    client = TestClient(app)
    response = client.get(f"/carrito/{sesion_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["sesion_id"] == sesion_id
    assert data["total"] == 1800000.0  # 900000 * 2

    app.dependency_overrides.clear()