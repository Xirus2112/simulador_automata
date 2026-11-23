from secrets import token_hex

from flask import Flask, render_template

from routes.main import rutas


def crear_app():
    app = Flask(__name__)
    app.config.update(SECRET_KEY=token_hex(32), MAX_CONTENT_LENGTH=4 * 1024 * 1024)
    # Aquí quedan los formularios que todavía no se han activado.
    app.extensions["borradores"] = {}
    app.register_blueprint(rutas)

    @app.errorhandler(413)
    def formulario_grande(_error):
        return render_template("aviso.html", mensaje="El envío supera el tamaño máximo de 4 MiB."), 413

    return app


if __name__ == "__main__":
    # El AFD se guarda en memoria. Si Flask reinicia el proceso, se pierde.
    crear_app().run(host="127.0.0.1", port=5000, use_reloader=False, threaded=False)
