from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/api/libros_antiguos')
def get_libros_antiguos():
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

if __name__ == '__main__':
    app.run(debug=True)
