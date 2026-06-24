import pytest
import httpx

# URL del sistema desplegado en Docker
BASE_URL = "http://localhost:8000"


@pytest.fixture(scope="module")
def cliente_http():
    """Cliente HTTP real que apunta a la API desplegada en contenedor."""
    with httpx.Client(base_url=BASE_URL, timeout=10.0) as client:
        yield client


def test_flujo_completo_carrito_dos_productos(cliente_http):
    """
    Flujo E2E completo a nivel de API:
    1. Agrega dos productos diferentes al carrito.
    2. Consulta el estado del carrito con GET.
    3. Valida que el total corresponde a la suma matemática esperada.
    """
    sesion_id = "sesion-sistema-e2e-001"

    # --- PASO 1: Agregar producto 1 ---
    producto_1 = {
        "nombre": "Monitor 4K",
        "precio": 1200000.0,
        "cantidad": 1
    }
    resp1 = cliente_http.post(
        f"/carrito/{sesion_id}/productos",
        json=producto_1
    )
    assert resp1.status_code == 201, f"Fallo al agregar producto 1: {resp1.text}"
    assert resp1.json()["mensaje"] == "Producto agregado"

    # --- PASO 2: Agregar producto 2 ---
    producto_2 = {
        "nombre": "Teclado Inalámbrico",
        "precio": 150000.0,
        "cantidad": 2
    }
    resp2 = cliente_http.post(
        f"/carrito/{sesion_id}/productos",
        json=producto_2
    )
    assert resp2.status_code == 201, f"Fallo al agregar producto 2: {resp2.text}"

    # --- PASO 3: Consultar el carrito ---
    resp_carrito = cliente_http.get(f"/carrito/{sesion_id}")
    assert resp_carrito.status_code == 200

    data = resp_carrito.json()
    assert data["sesion_id"] == sesion_id

    # --- PASO 4: Validar total matemáticamente ---
    # Monitor:  1200000 * 1 = 1200000
    # Teclado:   150000 * 2 =  300000
    # Total esperado:         1500000
    total_esperado = (producto_1["precio"] * producto_1["cantidad"]) + \
                     (producto_2["precio"] * producto_2["cantidad"])

    assert data["total"] == total_esperado, (
        f"Total incorrecto. Esperado: {total_esperado}, Obtenido: {data['total']}"
    )