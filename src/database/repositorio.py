from sqlalchemy.orm import Session
from src.database.models import CarritoDB, ItemCarritoDB


class CarritoRepositorio:
    def __init__(self, db: Session):
        self.db = db

    def _obtener_o_crear_carrito(self, sesion_id: str) -> CarritoDB:
        carrito = self.db.query(CarritoDB).filter(
            CarritoDB.sesion_id == sesion_id
        ).first()
        if not carrito:
            carrito = CarritoDB(sesion_id=sesion_id)
            self.db.add(carrito)
            self.db.flush()
        return carrito

    def agregar_item(
        self, sesion_id: str, nombre: str, precio: float, cantidad: int
    ) -> ItemCarritoDB:
        carrito = self._obtener_o_crear_carrito(sesion_id)
        item = ItemCarritoDB(
            carrito_id=carrito.id,
            nombre=nombre,
            precio=precio,
            cantidad=cantidad,
        )
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def calcular_total(self, sesion_id: str) -> float:
        carrito = self.db.query(CarritoDB).filter(
            CarritoDB.sesion_id == sesion_id
        ).first()
        if not carrito:
            return 0.0
        return sum(item.precio * item.cantidad for item in carrito.items)