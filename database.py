import sqlite3
from datetime import datetime

import click
from flask import current_app, g

RUTA_BD = "comunidad.db"


def obtener_bd():
    if "bd" not in g:
        g.bd = sqlite3.connect(current_app.config["RUTA_BD"])
        g.bd.row_factory = sqlite3.Row
        g.bd.execute("PRAGMA foreign_keys = ON")
    return g.bd


def cerrar_bd(e=None):
    bd = g.pop("bd", None)
    if bd is not None:
        bd.close()


def inicializar_bd():
    bd = obtener_bd()
    with current_app.open_resource("schema.sql") as f:
        bd.executescript(f.read().decode("utf8"))
    bd.commit()


def registrar_comandos(app):
    app.teardown_appcontext(cerrar_bd)
    app.cli.add_command(comando_init_db)


@click.command("init-db")
def comando_init_db():
    """Crea las tablas de la base de datos."""
    inicializar_bd()
    click.echo("Base de datos inicializada.")


def ahora():
    return datetime.utcnow().isoformat(timespec="seconds")
