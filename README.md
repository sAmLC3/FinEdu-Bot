# FinEdu-Bot

Proyecto base en Python para gestionar contratos en PostgreSQL con operaciones CRUD.

## Integrante

- Diogo Mauricio Canchari Soto - Backend

## Requisitos

- Python 3.12 o superior
- PostgreSQL disponible (local o en la nube)
- PowerShell (en Windows)

## Archivos importantes

- contratos_crud.py: clase con Create, Read, Update y Delete sobre la tabla contratos.
- .env.example: plantilla de variables de entorno.
- .gitignore: exclusiones para entorno Python y secretos.

## 1 Crear y activar entorno virtual

Desde la carpeta raíz del proyecto:

```powershell
python -m venv ..\.venv
..\.venv\Scripts\Activate.ps1
```

## 2 Instalar dependencias

```powershell
pip install psycopg2-binary python-dotenv
```

## 3 Configurar variables de entorno

Crear un archivo .env en la raíz del proyecto usando como referencia .env.example.

Contenido esperado:

```env
DB_HOST=
DB_PORT=5432
DB_NAME=
DB_USER=
DB_PASSWORD=
```

Notas:

- No subir .env al repositorio.
- El script carga automáticamente el archivo .env.

## 4 Ejecutar y verificar el CRUD

```powershell
Set-Location "c:\Users\User\Desktop\taller de proyectos\FinEdu-Bot"
python contratos_crud.py
```

Si termina con Exit Code 0, el CRUD está funcionando y sí se conecta a la base.

El script de ejemplo realiza:

- Create: inserta un contrato
- Read: lista todos y consulta por id
- Update: modifica monto
- Delete: elimina el contrato creado

## Errores comunes

1. Import could not be resolved
Causa: faltan paquetes en el entorno activo.
Acción: reinstalar dependencias dentro de ..\.venv.

2. relation contratos does not exist
Causa: la tabla no está creada en la base DB_NAME.
Acción: crear la tabla contratos en PostgreSQL antes de ejecutar el script.

