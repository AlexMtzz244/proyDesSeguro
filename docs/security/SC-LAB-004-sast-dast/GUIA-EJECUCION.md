# Guia de ejecucion - SC-LAB-004 SAST y DAST

## 1. Proposito

Este documento describe como preparar y ejecutar el laboratorio local de
SecureCampus. El proyecto demuestra dos controles de seguridad:

- **SAST:** Bandit revisa los archivos Python bajo `src/`.
- **DAST:** una prueba automatizada valida que `/buscar` codifica una carga XSS
  antes de mostrarla en HTML.

No se necesitan servicios externos ni credenciales. El servidor se limita a
`127.0.0.1`, por lo que solo queda accesible desde el equipo local.

## 2. Requisitos previos

- Windows con Python 3 instalado y disponible mediante el comando `py`.
- PowerShell.
- Acceso a Internet la primera vez, para descargar Flask y Bandit desde PyPI.

Compruebe la instalacion de Python:

```powershell
py --version
```

Si el comando no existe, instale Python 3 desde https://www.python.org/downloads/
y active la opcion **Add Python to PATH** durante la instalacion.

## 3. Preparar el entorno

Abra PowerShell en la raiz del repositorio y entre al directorio del laboratorio:

```powershell
cd "docs\security\SC-LAB-004-sast-dast"
py -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\python -m pip install -r requirements.txt
```

No es necesario activar el entorno virtual porque todos los comandos usan su
interprete de forma explicita. Si desea activarlo para una sesion interactiva:

```powershell
.\.venv\Scripts\Activate.ps1
```

Para cerrar una sesion activada:

```powershell
deactivate
```

Si PowerShell bloquea `Activate.ps1`, omita la activacion o permita scripts solo
para el proceso actual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 4. Ejecutar las validaciones

Ejecute los comandos desde `docs/security/SC-LAB-004-sast-dast`.

### 4.1 Comprobacion de sintaxis

```powershell
.\.venv\Scripts\python -m compileall -q src
```

El comando termina sin salida y con codigo de salida `0` cuando los archivos son
sintacticamente validos.

### 4.2 Analisis estatico (SAST)

```powershell
.\.venv\Scripts\python -m bandit -r src
```

Bandit analiza recursivamente `src/`. Revise el resumen final: cualquier hallazgo
debe evaluarse antes de dar por aceptada la practica. En particular, no sustituya
la consulta parametrizada de `src/app.py` por concatenacion de SQL ni active
`debug=True` en Flask.

### 4.3 Prueba dinamica (DAST)

```powershell
.\.venv\Scripts\python -m unittest discover -s tests -v
```

El resultado esperado contiene `test_search_escapes_html_supplied_by_the_user`
y termina con `OK`. La prueba envia `<script>alert(1)</script>` a `/buscar` y
confirma que se devuelve codificado, no como JavaScript ejecutable.

## 5. Ejecucion manual de la aplicacion web

Inicie el servidor Flask:

```powershell
.\.venv\Scripts\python src\webapp.py
```

Abra en el navegador:

```text
http://127.0.0.1:5000/
```

Para comprobar manualmente el manejo de HTML, visite:

```text
http://127.0.0.1:5000/buscar?nombre=%3Cscript%3Ealert(1)%3C%2Fscript%3E
```

La pagina debe mostrar el texto de la carga codificado. Detenga el servidor con
`Ctrl+C` en PowerShell.

## 6. Ejecucion del ejemplo SQLite

El archivo `src/app.py` solicita un nombre y ejecuta una consulta parametrizada
contra `securecampus.db` en el directorio actual. Para ejecutarlo se requiere una
base SQLite local con la tabla `estudiantes` y las columnas `id`, `nombre` y
`correo`:

```powershell
.\.venv\Scripts\python src\app.py
```

Este flujo no forma parte de la prueba DAST. Si la base no existe, SQLite creara
un archivo vacio y la consulta fallara porque no encontrara la tabla; ello no
afecta la ejecucion de Bandit, Flask ni las pruebas automatizadas.

## 7. Secuencia recomendada para evidencia

```powershell
.\.venv\Scripts\python -m compileall -q src
.\.venv\Scripts\python -m bandit -r src
.\.venv\Scripts\python -m unittest discover -s tests -v
```

Registre la fecha, el sistema operativo, la version de Python y las salidas de
estos tres comandos como evidencia de la practica.

## 8. Problemas frecuentes

| Situacion | Accion recomendada |
|---|---|
| `py` no se reconoce | Instale Python 3 y active `Add Python to PATH`; abra una nueva consola. |
| `No module named bandit` o `flask` | Repita `.\.venv\Scripts\python -m pip install -r requirements.txt`. |
| El puerto 5000 esta ocupado | Cierre el proceso que usa el puerto o cambie `port=5000` en `src/webapp.py` y use la nueva URL local. |
| `no such table: estudiantes` al usar `app.py` | Cree o proporcione `securecampus.db` con la tabla requerida; el resto del laboratorio no depende de ella. |
| Las pruebas no importan `src.webapp` | Confirme que el comando se ejecuta desde la carpeta de este laboratorio. |