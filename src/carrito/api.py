from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from src.database.config import get_db, init_db
from src.database.repositorio import CarritoRepositorio
from pydantic import BaseModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="TiendaUV - Carrito de Compras", lifespan=lifespan)


class ProductoInput(BaseModel):
    nombre: str
    precio: float
    cantidad: int


@app.post("/carrito/{sesion_id}/productos", status_code=201)
def agregar_producto(
    sesion_id: str,
    producto: ProductoInput,
    db: Session = Depends(get_db)
):
    repo = CarritoRepositorio(db)
    item = repo.agregar_item(
        sesion_id, producto.nombre, producto.precio, producto.cantidad
    )
    return {"mensaje": "Producto agregado", "item_id": item.id}


@app.get("/carrito/{sesion_id}", status_code=200)
def obtener_carrito(sesion_id: str, db: Session = Depends(get_db)):
    repo = CarritoRepositorio(db)
    total = repo.calcular_total(sesion_id)
    return {"sesion_id": sesion_id, "total": total}