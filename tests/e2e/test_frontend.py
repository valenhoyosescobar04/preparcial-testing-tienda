import pytest
from playwright.sync_api import Page, expect


def test_agregar_producto_y_verificar_total(page: Page):
    """
    Automatiza el flujo completo en el frontend Angular:
    1. Navega a /carrito
    2. Llena el formulario con Monitor, 1500000, cantidad 1
    3. Hace clic en agregar
    4. Verifica que el total muestra 1.500.000
    """
    # 1. Navegar a la ruta del carrito
    page.goto("http://localhost:4200/carrito")

    # 2. Llenar el formulario usando data-testid
    page.get_by_test_id("input-nombre-producto").fill("Monitor")
    page.get_by_test_id("input-precio-producto").fill("1500000")
    page.get_by_test_id("input-cantidad-producto").fill("1")

    # 3. Hacer clic en el botón de agregar
    page.get_by_test_id("btn-agregar-producto").click()

    # 4. Esperar dinámicamente y verificar el total
    total_elemento = page.get_by_test_id("total-carrito")
    expect(total_elemento).to_contain_text("1.500.000")