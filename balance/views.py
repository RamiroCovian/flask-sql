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


@app.route("/nuevo/", methods=["GET", "POST"])
def agregar(fecha, concepto, tipo, cantidad):
    db = DBManager(RUTA)
    ha_ido_bien = db.insertar(fecha, concepto, tipo, cantidad)
    movimiento = {}
    formulario = MovimientoForm(data=movimiento)
    return render_template("nuevo.html", form=formulario, resultado=ha_ido_bien)


@app.route("/borrar/<int:id>")
def eliminar(id):
    db = DBManager(RUTA)
    ha_ido_bien = db.borrar(id)
    return render_template("borrado.html", resultado=ha_ido_bien)


@app.route("/editar/<int:id>")
def actualizar(id):
    if request.method == "GET":
        db = DBManager(RUTA)
        movimiento = db.obtenerMovimiento(id)
        # TODO: Acceder aqui por un enlace en la lista de movimientos
        # (Al lado del boton de eliminar)
        formulario = MovimientoForm(data=movimiento)
        return render_template("form_movimiento.html", form=formulario)
    if request.method == "POST":
        db = DBManager(RUTA)
        ha_ido_bien = db.modificar()
        movimiento = {}
        formulario = MovimientoForm(data=movimiento)
        return render_template("agregado.html", resultado=ha_ido_bien)

    return f"TODO: tratar el metodo POST para actualizar el movimiento {id}"
