from flask import Flask,request,render_template,send_file
from rembg import remove
import io
import uuid



app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/subir_img", methods=["GET"])
def subir_img():
    return render_template("subir_img.html")


@app.route("/remove_bg", methods=["POST"])
def remove_bg():
    if 'image' not in request.files:
        return "No se envió ninguna imagen", 400
    
    file = request.files['image']
    
    if file.filename == '':
        return "No se seleccionó archivo", 400
    
    # Leer la imagen
    input_data = file.read()
    
    # Eliminar el fondo
    output_data = remove(input_data)
    
    # Generar ID único y obtener nombre original
    unique_id = str(uuid.uuid4())[:8]
    original_name = file.filename.rsplit('.', 1)[0]
    new_filename = f'{original_name}_rendx_{unique_id}.png'
    
    # Retornar la imagen sin fondo
    return send_file(
        io.BytesIO(output_data),
        mimetype='image/png',
        as_attachment=True,
        download_name=new_filename
    )


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return render_template('404.html'), 405




if __name__ == '__main__':

    app.run(debug=True)
