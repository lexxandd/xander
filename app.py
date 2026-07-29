from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash

from database import obtener_bd, inicializar_bd, registrar_comandos, ahora
from contenido import VENTAJAS, DESVENTAJAS, DISTROS, CATEGORIAS, RECURSOS

app = Flask(__name__)
app.config["SECRET_KEY"] = "cambia-esta-clave-en-produccion"
app.config["RUTA_BD"] = "comunidad.db"

registrar_comandos(app)


# ---------- Usuario actual (basado en sesión) ----------

@app.before_request
def cargar_usuario_actual():
    usuario_id = session.get("usuario_id")
    if usuario_id is None:
        g.usuario = None
    else:
        bd = obtener_bd()
        g.usuario = bd.execute(
            "SELECT * FROM usuarios WHERE id = ?", (usuario_id,)
        ).fetchone()


@app.context_processor
def inyectar_usuario():
    # Hace que {{ usuario }} y {{ usuario_es_lider }} estén disponibles en todas las plantillas
    return {"usuario": g.get("usuario"), "usuario_es_lider": es_lider()}


def login_requerido(vista):
    @wraps(vista)
    def envoltura(*args, **kwargs):
        if g.usuario is None:
            flash("Inicia sesión para continuar.", "error")
            return redirect(url_for("login", next=request.path))
        return vista(*args, **kwargs)
    return envoltura


def es_lider():
    return g.usuario is not None and g.usuario["rol"] == "líder"


# ---------- Páginas de contenido ----------

@app.route("/")
def inicio():
    bd = obtener_bd()
    total_usuarios = bd.execute("SELECT COUNT(*) AS n FROM usuarios").fetchone()["n"]
    total_publicaciones = bd.execute("SELECT COUNT(*) AS n FROM publicaciones").fetchone()["n"]
    return render_template(
        "index.html",
        ventajas=VENTAJAS[:3],
        distros=DISTROS[:3],
        total_usuarios=total_usuarios,
        total_publicaciones=total_publicaciones,
    )


@app.route("/ventajas-desventajas")
def ventajas_desventajas():
    return render_template("ventajas.html", ventajas=VENTAJAS, desventajas=DESVENTAJAS)


@app.route("/distros")
def distros():
    return render_template("distros.html", distros=DISTROS)


@app.route("/recursos")
def recursos():
    return render_template("recursos.html", recursos=RECURSOS)


# ---------- Autenticación ----------

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if g.usuario is not None:
        return redirect(url_for("comunidad"))

    if request.method == "POST":
        nombre_usuario = request.form.get("nombre_usuario", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        distro_favorita = request.form.get("distro_favorita", "").strip()
        bd = obtener_bd()
        error = None

        if not nombre_usuario or not email or not password:
            error = "Completa todos los campos obligatorios."
        elif bd.execute(
            "SELECT id FROM usuarios WHERE nombre_usuario = ?", (nombre_usuario,)
        ).fetchone():
            error = "Ese nombre de usuario ya está en uso."
        elif bd.execute("SELECT id FROM usuarios WHERE email = ?", (email,)).fetchone():
            error = "Ese correo ya está registrado."

        if error:
            flash(error, "error")
            return render_template("registro.html")

        es_primer_usuario = bd.execute("SELECT COUNT(*) AS n FROM usuarios").fetchone()["n"] == 0
        rol = "líder" if es_primer_usuario else "miembro"

        cursor = bd.execute(
            "INSERT INTO usuarios (nombre_usuario, email, password_hash, distro_favorita, rol, creado_en) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (nombre_usuario, email, generate_password_hash(password), distro_favorita, rol, ahora()),
        )
        bd.commit()
        session.clear()
        session["usuario_id"] = cursor.lastrowid
        if es_primer_usuario:
            flash("¡Cuenta creada! Como fuiste el primer registro, eres líder de la comunidad.", "success")
        else:
            flash("¡Cuenta creada! Bienvenido a la comunidad.", "success")
        return redirect(url_for("comunidad"))

    return render_template("registro.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if g.usuario is not None:
        return redirect(url_for("comunidad"))

    if request.method == "POST":
        nombre_usuario = request.form.get("nombre_usuario", "").strip()
        password = request.form.get("password", "")
        bd = obtener_bd()
        usuario = bd.execute(
            "SELECT * FROM usuarios WHERE nombre_usuario = ?", (nombre_usuario,)
        ).fetchone()

        if usuario and check_password_hash(usuario["password_hash"], password):
            session.clear()
            session["usuario_id"] = usuario["id"]
            flash(f"Bienvenido de nuevo, {usuario['nombre_usuario']}.", "success")
            siguiente = request.args.get("next")
            return redirect(siguiente or url_for("comunidad"))

        flash("Usuario o contraseña incorrectos.", "error")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada.", "success")
    return redirect(url_for("inicio"))


# ---------- Comunidad ----------

@app.route("/comunidad")
def comunidad():
    bd = obtener_bd()
    publicaciones = bd.execute(
        "SELECT p.*, u.nombre_usuario, u.rol, "
        "(SELECT COUNT(*) FROM comentarios c WHERE c.publicacion_id = p.id) AS total_comentarios, "
        "(SELECT COUNT(*) FROM me_gusta m WHERE m.publicacion_id = p.id) AS total_likes "
        "FROM publicaciones p JOIN usuarios u ON p.autor_id = u.id "
        "ORDER BY p.fijado DESC, p.creado_en DESC"
    ).fetchall()
    return render_template("comunidad.html", publicaciones=publicaciones)


@app.route("/comunidad/nueva", methods=["GET", "POST"])
@login_requerido
def nueva_publicacion():
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        contenido = request.form.get("contenido", "").strip()
        categoria = request.form.get("categoria", "").strip()

        if categoria not in CATEGORIAS:
            categoria = CATEGORIAS[0]

        if not titulo or not contenido:
            flash("El título y el contenido son obligatorios.", "error")
            return render_template("nueva_publicacion.html", categorias=CATEGORIAS)

        bd = obtener_bd()
        cursor = bd.execute(
            "INSERT INTO publicaciones (titulo, contenido, categoria, autor_id, creado_en) "
            "VALUES (?, ?, ?, ?, ?)",
            (titulo, contenido, categoria, g.usuario["id"], ahora()),
        )
        bd.commit()
        flash("Publicación creada.", "success")
        return redirect(url_for("ver_publicacion", publicacion_id=cursor.lastrowid))

    return render_template("nueva_publicacion.html", categorias=CATEGORIAS)


@app.route("/comunidad/<int:publicacion_id>", methods=["GET", "POST"])
def ver_publicacion(publicacion_id):
    bd = obtener_bd()

    if request.method == "POST":
        if g.usuario is None:
            flash("Inicia sesión para comentar.", "error")
            return redirect(url_for("login", next=request.path))

        contenido = request.form.get("contenido", "").strip()
        if contenido:
            bd.execute(
                "INSERT INTO comentarios (contenido, autor_id, publicacion_id, creado_en) VALUES (?, ?, ?, ?)",
                (contenido, g.usuario["id"], publicacion_id, ahora()),
            )
            bd.commit()
        return redirect(url_for("ver_publicacion", publicacion_id=publicacion_id))

    publicacion = bd.execute(
        "SELECT p.*, u.nombre_usuario, u.rol FROM publicaciones p "
        "JOIN usuarios u ON p.autor_id = u.id WHERE p.id = ?",
        (publicacion_id,),
    ).fetchone()

    if publicacion is None:
        flash("Esa publicación no existe.", "error")
        return redirect(url_for("comunidad"))

    comentarios = bd.execute(
        "SELECT c.*, u.nombre_usuario, u.rol FROM comentarios c "
        "JOIN usuarios u ON c.autor_id = u.id "
        "WHERE c.publicacion_id = ? ORDER BY c.creado_en ASC",
        (publicacion_id,),
    ).fetchall()

    total_likes = bd.execute(
        "SELECT COUNT(*) AS n FROM me_gusta WHERE publicacion_id = ?", (publicacion_id,)
    ).fetchone()["n"]

    ya_dio_like = False
    if g.usuario is not None:
        ya_dio_like = bd.execute(
            "SELECT 1 FROM me_gusta WHERE publicacion_id = ? AND usuario_id = ?",
            (publicacion_id, g.usuario["id"]),
        ).fetchone() is not None

    return render_template(
        "publicacion.html",
        publicacion=publicacion,
        comentarios=comentarios,
        total_likes=total_likes,
        ya_dio_like=ya_dio_like,
    )


@app.route("/comunidad/<int:publicacion_id>/like", methods=["POST"])
@login_requerido
def alternar_like(publicacion_id):
    bd = obtener_bd()

    publicacion = bd.execute(
        "SELECT id FROM publicaciones WHERE id = ?", (publicacion_id,)
    ).fetchone()
    if publicacion is None:
        flash("Esa publicación no existe.", "error")
        return redirect(url_for("comunidad"))

    ya_existe = bd.execute(
        "SELECT 1 FROM me_gusta WHERE publicacion_id = ? AND usuario_id = ?",
        (publicacion_id, g.usuario["id"]),
    ).fetchone()

    if ya_existe:
        bd.execute(
            "DELETE FROM me_gusta WHERE publicacion_id = ? AND usuario_id = ?",
            (publicacion_id, g.usuario["id"]),
        )
    else:
        bd.execute(
            "INSERT INTO me_gusta (usuario_id, publicacion_id, creado_en) VALUES (?, ?, ?)",
            (g.usuario["id"], publicacion_id, ahora()),
        )
    bd.commit()
    return redirect(url_for("ver_publicacion", publicacion_id=publicacion_id))


@app.route("/comunidad/<int:publicacion_id>/eliminar", methods=["POST"])
@login_requerido
def eliminar_publicacion(publicacion_id):
    bd = obtener_bd()
    publicacion = bd.execute(
        "SELECT * FROM publicaciones WHERE id = ?", (publicacion_id,)
    ).fetchone()

    if publicacion is None:
        flash("Esa publicación no existe.", "error")
        return redirect(url_for("comunidad"))

    if publicacion["autor_id"] != g.usuario["id"] and not es_lider():
        flash("No tienes permiso para eliminar esa publicación.", "error")
        return redirect(url_for("ver_publicacion", publicacion_id=publicacion_id))

    bd.execute("DELETE FROM me_gusta WHERE publicacion_id = ?", (publicacion_id,))
    bd.execute("DELETE FROM comentarios WHERE publicacion_id = ?", (publicacion_id,))
    bd.execute("DELETE FROM publicaciones WHERE id = ?", (publicacion_id,))
    bd.commit()
    flash("Publicación eliminada.", "success")
    return redirect(url_for("comunidad"))


@app.route("/comunidad/<int:publicacion_id>/comentario/<int:comentario_id>/eliminar", methods=["POST"])
@login_requerido
def eliminar_comentario(publicacion_id, comentario_id):
    bd = obtener_bd()
    comentario = bd.execute(
        "SELECT * FROM comentarios WHERE id = ? AND publicacion_id = ?",
        (comentario_id, publicacion_id),
    ).fetchone()

    if comentario is None:
        flash("Ese comentario no existe.", "error")
        return redirect(url_for("ver_publicacion", publicacion_id=publicacion_id))

    if comentario["autor_id"] != g.usuario["id"] and not es_lider():
        flash("No tienes permiso para eliminar ese comentario.", "error")
        return redirect(url_for("ver_publicacion", publicacion_id=publicacion_id))

    bd.execute("DELETE FROM comentarios WHERE id = ?", (comentario_id,))
    bd.commit()
    flash("Comentario eliminado.", "success")
    return redirect(url_for("ver_publicacion", publicacion_id=publicacion_id))


@app.route("/comunidad/<int:publicacion_id>/fijar", methods=["POST"])
@login_requerido
def alternar_fijado(publicacion_id):
    if not es_lider():
        flash("Solo un líder de la comunidad puede fijar publicaciones.", "error")
        return redirect(url_for("ver_publicacion", publicacion_id=publicacion_id))

    bd = obtener_bd()
    publicacion = bd.execute(
        "SELECT fijado FROM publicaciones WHERE id = ?", (publicacion_id,)
    ).fetchone()

    if publicacion is None:
        flash("Esa publicación no existe.", "error")
        return redirect(url_for("comunidad"))

    nuevo_valor = 0 if publicacion["fijado"] else 1
    bd.execute("UPDATE publicaciones SET fijado = ? WHERE id = ?", (nuevo_valor, publicacion_id))
    bd.commit()
    flash("Publicación fijada." if nuevo_valor else "Publicación desfijada.", "success")
    return redirect(url_for("ver_publicacion", publicacion_id=publicacion_id))


# ---------- Perfil de usuario ----------

@app.route("/perfil/<nombre_usuario>")
def perfil(nombre_usuario):
    bd = obtener_bd()
    usuario_perfil = bd.execute(
        "SELECT * FROM usuarios WHERE nombre_usuario = ?", (nombre_usuario,)
    ).fetchone()

    if usuario_perfil is None:
        flash("Ese usuario no existe.", "error")
        return redirect(url_for("comunidad"))

    publicaciones = bd.execute(
        "SELECT p.*, "
        "(SELECT COUNT(*) FROM comentarios c WHERE c.publicacion_id = p.id) AS total_comentarios, "
        "(SELECT COUNT(*) FROM me_gusta m WHERE m.publicacion_id = p.id) AS total_likes "
        "FROM publicaciones p WHERE p.autor_id = ? ORDER BY p.creado_en DESC",
        (usuario_perfil["id"],),
    ).fetchall()

    return render_template(
        "perfil.html", usuario_perfil=usuario_perfil, publicaciones=publicaciones
    )


with app.app_context():
    inicializar_bd()
app.run(host='0.0.0.0', port=5000, debug=True)

