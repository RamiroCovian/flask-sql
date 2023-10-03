import os
from datetime import date
from flask import render_template, request
from . import app, RUTA
from .forms import MovimientoForm
from .models import DBManager


@app.route("/")
def home():
    db = DBManager(RUTA)
    sql = "SELECT id, fecha, concepto, tipo, cantidad FROM movimientos"
    movimientos = db.consultaSQL(sql)
    return render_template("inicio.html", movs=movimientos)


@app.route("/borrar/<int:id>")
def eliminar(id):
    db = DBManager(RUTA)
    ha_ido_bien = db.borrar(id)
    return render_template("borrado.html", resultado=ha_ido_bien)


@app.route("/editar/<int:id>")
def actualizar(id):
    if request.method == "GET":
        # TODO: Obtener el movimiento que se va a editar por si ID
        # SELECT id, fecha, concepto, tipo, cantidad FROM movimientos WHERE id=?
        # TODO: Acceder aqui por un enlace en la lista de movimientos
        # (Al lado del boton de eliminar)
        movimiento = {
            "id": 55,
            "fecha": date.fromisoformat("2023-10-03"),
            "concepto": "Curso de formularios en Python",
            "tipo": "G",
            "cantidad": 55.95,
        }
        formulario = MovimientoForm(data=movimiento)
        return render_template("form_movimiento.html", form=formulario)
    return f"TODO: tratar el metodo POST para actualizar el movimiento {id}"
