FROM python:3.12-slim

WORKDIR /app

# Instalar uv
RUN pip install uv

COPY pyproject.toml .
RUN uv pip install --system --no-cache .

COPY src/ ./src/

EXPOSE 8000

CMD ["uvicorn", "src.carrito.api:app", "--host", "0.0.0.0", "--port", "8000"]