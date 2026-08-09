import os
from datetime import date
from decimal import Decimal
from typing import Any, Dict, List, Optional

import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv


load_dotenv()


class ContratosCRUD:
    """CRUD para la tabla contratos usando psycopg2 y variables de entorno."""

    def __init__(self) -> None:
        required_env = ["DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"]
        missing = [key for key in required_env if not os.environ.get(key)]
        if missing:
            raise ValueError(
                "Faltan variables de entorno para la conexion: " + ", ".join(missing)
            )

        self._conn_params = {
            "host": os.environ["DB_HOST"],
            "port": os.environ["DB_PORT"],
            "dbname": os.environ["DB_NAME"],
            "user": os.environ["DB_USER"],
            "password": os.environ["DB_PASSWORD"],
            "sslmode": "require"
        }

    def _get_connection(self):
        return psycopg2.connect(**self._conn_params)

    def create(self, titulo: str, monto: Decimal, fecha: date) -> Dict[str, Any]:
        query = """
            INSERT INTO contratos (titulo, monto, fecha)
            VALUES (%s, %s, %s)
            RETURNING id, titulo, monto, fecha;
        """
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, (titulo, monto, fecha))
                contrato = cur.fetchone()
        return dict(contrato)

    def read_all(self) -> List[Dict[str, Any]]:
        query = """
            SELECT id, titulo, monto, fecha
            FROM contratos
            ORDER BY id;
        """
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                rows = cur.fetchall()
        return [dict(row) for row in rows]

    def read_by_id(self, contrato_id: int) -> Optional[Dict[str, Any]]:
        query = """
            SELECT id, titulo, monto, fecha
            FROM contratos
            WHERE id = %s;
        """
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, (contrato_id,))
                row = cur.fetchone()
        return dict(row) if row else None

    def update(
        self,
        contrato_id: int,
        titulo: Optional[str] = None,
        monto: Optional[Decimal] = None,
        fecha: Optional[date] = None,
    ) -> Optional[Dict[str, Any]]:
        fields = []
        values = []

        if titulo is not None:
            fields.append("titulo = %s")
            values.append(titulo)
        if monto is not None:
            fields.append("monto = %s")
            values.append(monto)
        if fecha is not None:
            fields.append("fecha = %s")
            values.append(fecha)

        if not fields:
            raise ValueError("Debes enviar al menos un campo para actualizar.")

        query = f"""
            UPDATE contratos
            SET {", ".join(fields)}
            WHERE id = %s
            RETURNING id, titulo, monto, fecha;
        """
        values.append(contrato_id)

        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, tuple(values))
                updated = cur.fetchone()
        return dict(updated) if updated else None

    def delete(self, contrato_id: int) -> bool:
        query = """
            DELETE FROM contratos
            WHERE id = %s
            RETURNING id;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (contrato_id,))
                deleted = cur.fetchone()
        return deleted is not None


if __name__ == "__main__":
    # Ejemplo de uso rapido.
    # Requiere variables de entorno: DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
    crud = ContratosCRUD()
    nuevo = crud.create("Contrato de servicios", Decimal("15000.50"), date.today())
    print("Creado:", nuevo)

    todos = crud.read_all()
    print("Todos:", todos)

    contrato = crud.read_by_id(nuevo["id"])
    print("Por ID:", contrato)

    actualizado = crud.update(nuevo["id"], monto=Decimal("17500.00"))
    print("Actualizado:", actualizado)

    eliminado = crud.delete(nuevo["id"])
    print("Eliminado:", eliminado)
