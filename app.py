from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

# Configuración para permitir solicitudes CORS desde cualquier origen
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/api/libros_antiguo')
def get_libros_antiguo():
    try:
        # Conecta a la base de datos SQLite
        conn = sqlite3.connect('biblia.db')
        cursor = conn.cursor()

        # Realiza la consulta
        cursor.execute("SELECT id_libro, abreviacion, qnt_capitulos, nombre FROM libros WHERE testamento = 'Antiguo'")
        libros = cursor.fetchall()

        # Crea una lista de diccionarios para el resultado JSON
        libros_json = [{'id_libro': row[0], 'abreviacion': row[1], 'qnt_capitulos': row[2], 'nombre': row[3]} for row in libros]

        return jsonify(libros_json)

    except Exception as e:
        return jsonify({'error': str(e)}), 500        

@app.route('/api/libros_nuevo')
def get_libros_nuevos():
    try:
        # Conecta a la base de datos SQLite
        conn = sqlite3.connect('biblia.db')
        cursor = conn.cursor()

        # Realiza la consulta
        cursor.execute("SELECT id_libro, abreviacion, qnt_capitulos, nombre FROM libros WHERE testamento = 'Nuevo'")
        libros = cursor.fetchall()

        # Crea una lista de diccionarios para el resultado JSON
        libros_json = [{'id_libro': row[0], 'abreviacion': row[1], 'qnt_capitulos': row[2], 'nombre': row[3]} for row in libros]

        return jsonify(libros_json)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/libros/<int:id_libro>')
def get_libro(id_libro):
    try:
        # Conecta a la base de datos SQLite
        conn = sqlite3.connect('biblia.db')
        cursor = conn.cursor()

        # Realiza la consulta
        cursor.execute("""SELECT id_libro, abreviacion, qnt_capitulos, nombre FROM libros WHERE id_libro = ?""",(id_libro,))
        libros = cursor.fetchall()

        # Crea una lista de diccionarios para el resultado JSON
        libros_json = [{'id_libro': row[0], 'abreviacion': row[1], 'qnt_capitulos': row[2], 'nombre': row[3]} for row in libros]

        return jsonify(libros_json)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/librosnombre/<string:nombre_libro>')
def get_libronombre(nombre_libro):
    try:
        # Conecta a la base de datos SQLite
        conn = sqlite3.connect('biblia.db')
        cursor = conn.cursor()

        # Realiza la consulta
        cursor.execute("""SELECT id_libro, abreviacion, qnt_capitulos, nombre, testamento FROM libros WHERE nombre LIKE ?""", ('%' + nombre_libro + '%',))
        libros = cursor.fetchall()

        # Crea una lista de diccionarios para el resultado JSON
        libros_json = [{'id_libro': row[0], 'abreviacion': row[1], 'qnt_capitulos': row[2], 'nombre': row[3], 'testamento': row[4]} for row in libros]

        return jsonify(libros_json)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Endpoint para obtener los versículos de un libro específico
@app.route('/api/versiculos_por_libro/<int:id_libro>')
def get_versiculos_por_libro(id_libro):
    try:
        conn = sqlite3.connect('biblia.db')
        cursor = conn.cursor()
        cursor.execute("""SELECT v.id_versiculo, c.numero_capitulo, v.num_versiculo, v.texto
                          FROM libros l
                          INNER JOIN capitulos c ON c.id_libro = l.id_libro
                          INNER JOIN versiculos v ON v.id_capitulo = c.id_capitulo
                          WHERE l.id_libro = ? order by c.numero_capitulo, v.num_versiculo""", (id_libro,))
        versiculos = cursor.fetchall()
        versiculos_json = [{'id_versiculo': row[0], 'numero_capitulo': row[1], 'num_versiculo': row[2], 'texto': row[3]} for row in versiculos]
        return jsonify(versiculos_json)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=8080)
