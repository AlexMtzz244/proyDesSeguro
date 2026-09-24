from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>SecureCampus Security Lab</title>
</head>
<body>
    <h1>SecureCampus</h1>
    <h2>Security Lab</h2>
    <p>Aplicacion local para practicas de Desarrollo Seguro.</p>
    <form method="GET" action="/buscar">
        <label for="nombre">Buscar estudiante:</label>
        <input type="text" id="nombre" name="nombre">
        <button type="submit">Buscar</button>
    </form>
</body>
</html>
"""


@app.route("/")
def inicio():
    return render_template_string(HTML)


@app.route("/buscar")
def buscar():
    nombre = request.args.get("nombre", "")
    resultado_html = """
    <html>
        <head>
            <title>Resultado - SecureCampus</title>
        </head>
        <body>
            <h1>Resultado de busqueda</h1>
            <p>Estudiante buscado: {{ nombre }}</p>
            <a href="/">Regresar</a>
        </body>
    </html>
    """
    return render_template_string(resultado_html, nombre=nombre)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)