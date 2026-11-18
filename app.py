from flask import Flask, redirect, render_template, request, url_for

from bd import db


def create_app():
    app = Flask(__name__)
    db.init_db()

    @app.get("/participa")
    def participa():
        return render_template("participa.html")

    @app.post("/mural")
    def enviar_mural():
        texto = request.form.get("texto", "").strip()
        if not texto:
            return render_template("participa.html", error_message="Escribe un mensaje antes de enviarlo."), 400
        if len(texto) > 200:
            return render_template("participa.html", error_message="El mensaje no puede superar los 200 caracteres."), 400

        db.insertar_mural(texto)
        return redirect(url_for("gracias"))
    
    @app.post("/foro")
    def enviar_foro():
        titulo = request.form.get("titulo", "").strip()
        texto = request.form.get("texto", "").strip()

        if not titulo:
            error_message = "Escribe un título antes de enviar la reflexión."
        elif len(titulo) > 80:
            error_message = "El título no puede superar los 80 caracteres."
        elif not texto:
            error_message = "Escribe una reflexión antes de enviarla."
        elif len(texto) > 1000:
            error_message = "La reflexión no puede superar los 1000 caracteres."
        else:
            error_message = None

        if error_message:
            return render_template( "templates/participa.html", error_message=error_message,), 400

        db.insertar_foro(titulo, texto)
        return redirect(url_for("gracias"))
    
    @app.get("/gracias")
    def gracias():
        return render_template("gracias.html")

    return app

app = create_app()


if __name__ == "__main__":
    app.run()
