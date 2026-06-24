import pytest
from src.database.repositorio import CarritoRepositorio
from src.database.models import CarritoDB, ItemCarritoDB


def test_agregar_item_persiste_en_base_de_datos(db_session):
    """
    Verifica que agregar_item persiste físicamente los datos
    en PostgreSQL y devuelve el objeto CarritoDB correcto.
    """
    repo = CarritoRepositorio(db_session)
    sesion_id = "sesion-integracion-001"

    item = repo.agregar_item(
        sesion_id=sesion_id,
        nombre="Teclado Mecánico",
        precio=250000.0,
        cantidad=2
    )

    # Verificar que el item tiene ID asignado (persistido)
    assert item.id is not None
    assert item.nombre == "Teclado Mecánico"
    assert item.precio == 250000.0
    assert item.cantidad == 2

    # Verificar que el CarritoDB fue creado y vinculado
    carrito_en_db = db_session.query(CarritoDB).filter(
        CarritoDB.sesion_id == sesion_id
    ).first()

    assert carrito_en_db is not None
    assert carrito_en_db.sesion_id == sesion_id
    assert len(carrito_en_db.items) == 1
    assert carrito_en_db.items[0].nombre == "Teclado Mecánico"


def test_calcular_total_suma_correctamente(db_session):
    """Verifica que el total se calcula multiplicando precio x cantidad."""
    repo = CarritoRepositorio(db_session)
    sesion_id = "sesion-total-002"

    repo.agregar_item(sesion_id, "Mouse", 80000.0, 1)
    repo.agregar_item(sesion_id, "Pad", 20000.0, 3)

    total = repo.calcular_total(sesion_id)

    # Mouse: 80000 * 1 = 80000
    # Pad:   20000 * 3 = 60000
    # Total esperado:   140000
    assert total == 140000.0


def test_carrito_vacio_retorna_total_cero(db_session):
    """Un carrito inexistente debe retornar 0.0 como total."""
    repo = CarritoRepositorio(db_session)
    total = repo.calcular_total("sesion-inexistente-999")
    assert total == 0.0