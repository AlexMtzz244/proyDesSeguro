# SC-LAB-004 - SAST y DAST

| | |
|---|---|
| **Proyecto** | SecureCampus |
| **Curso** | Desarrollo Seguro |
| **Practica** | SC-LAB-004 |
| **Version** | 1.0 |
| **Fecha** | 23 de septiembre de 2026 |

## Integrantes del equipo

| Integrante | Matricula |
|---|---|
| Cesar Adan De La Cruz Moctezuma | _(completar)_ |
| Diego Salazar Reyes | _(completar)_ |
| Juan Pablo Castillo Angeles | _(completar)_ |
| Alejandro Martinez | _(completar)_ |

---

## 1. Objetivo y alcance

Este miniproyecto conserva de forma aislada el codigo entregado para el laboratorio
de SecureCampus y registra evidencia reproducible de dos actividades complementarias:

- **SAST**: Bandit inspecciona `src/` sin ejecutar el programa para detectar patrones
  inseguros en Python.
- **DAST**: una prueba de caja negra usa el cliente HTTP de Flask contra la ruta
  `/buscar` y verifica que una entrada HTML hostil no se refleje como marcado ejecutable.

El alcance se limita a `src/app.py` y `src/webapp.py`. No se analiza la aplicacion
academica principal ni se usan datos reales.

## 2. Estructura y ejecucion

```text
SC-LAB-004-sast-dast/
|- src/                    Codigo analizado
|- tests/                  Prueba dinamica de regresion
|- requirements.txt        Dependencias reproducibles
`- README.md               Evidencia y resultados
```

Desde esta carpeta, crear un entorno aislado y ejecutar:

```powershell
py -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m bandit -r src
.\.venv\Scripts\python -m unittest discover -s tests -v
```

Para una inspeccion manual con proxy de pruebas, ejecutar:

```powershell
.\.venv\Scripts\python src\webapp.py
```

La aplicacion queda limitada a `127.0.0.1:5000`; la solicitud de prueba es:

```text
http://127.0.0.1:5000/buscar?nombre=%3Cscript%3Ealert(1)%3C%2Fscript%3E
```

## 3. Evidencia SAST

### Inspeccion de la consulta SQLite

`src/app.py` consulta al estudiante mediante un marcador posicional y pasa el valor
como parametro separado:

```python
consulta = "SELECT id, nombre, correo FROM estudiantes WHERE nombre = ?"
cursor.execute(consulta, (nombre,))
```

El dato controlado por el usuario no se concatena al texto SQL. Esto evita que una
carga como `' OR '1'='1` cambie la estructura de la consulta. Es importante mantener
esta separacion: reemplazarla por interpolacion o concatenacion debe considerarse una
regresion de severidad alta (CWE-89).

### Inspeccion de configuracion Flask

`src/webapp.py` inicia con `debug=False` y escucha solo en `127.0.0.1`. Por tanto, el
laboratorio no expone el depurador interactivo ni publica el servidor en interfaces de
red durante la ejecucion local.

El comando Bandit queda incluido como evidencia repetible. El entorno base de la
sesion no tenia Bandit ni Flask instalados; por eso `requirements.txt` fija las
herramientas necesarias y no se declara un resultado de Bandit que no haya sido
producido en un entorno con esas dependencias.

## 4. Evidencia DAST

La prueba `tests/test_webapp_security.py` realiza una solicitud real a la ruta de
busqueda con el valor `<script>alert(1)</script>` y valida tres condiciones:

1. La respuesta HTTP es `200`.
2. La respuesta no incluye la etiqueta `script` sin escapar.
3. La respuesta muestra el contenido codificado como `&lt;script&gt;...`.

La plantilla usa `{{ nombre }}`, por lo que Jinja aplica autoescape a la salida HTML.
La prueba no intenta explotar ni atacar servicios externos: valida de forma local que
la entrada no se convierta en JavaScript ejecutable (CWE-79).

## 5. Resultados y criterio de aceptacion

| Evidencia | Resultado esperado | Criterio |
|---|---|---|
| Compilacion | `py -m compileall -q src` termina sin errores | El codigo copiado es sintacticamente valido. |
| SAST | Bandit revisa todo `src/` | No se aceptan concatenaciones de SQL ni modo debug expuesto. |
| DAST | La prueba XSS termina en verde | La carga se refleja codificada, no ejecutable. |
| Aislamiento | Servidor local en `127.0.0.1` | No se requiere exponer el laboratorio a la red. |

## 6. Criterios de aceptacion

- [x] El miniproyecto se encuentra aislado en `docs/security/SC-LAB-004-sast-dast/`.
- [x] El codigo fuente analizado se conserva bajo `src/`.
- [x] El analisis estatico es reproducible mediante Bandit.
- [x] La prueba dinamica verifica una carga XSS local y controlada.
- [x] Las dependencias y los comandos de evidencia estan versionados.