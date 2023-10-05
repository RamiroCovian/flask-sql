import os
from datetime import date
from flask import flash, redirect, render_template, request, url_for
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
def crear_movimiento():
    # TODO: reutilizar el formulario para crear movimientos nuevos
    # Reestructurar el codigo en models.py
    pass


@app.route("/borrar/<int:id>")
def eliminar(id):
    db = DBManager(RUTA)
    ha_ido_bien = db.borrar(id)
    # TODO: en lugar de volver a otra pantalla, pintar el mensaje con su propia plantilla
    # usar un mensaje flash y volver al listado
    # TODO: un poco mas dficil? pedir confirmacion antes de eliminar un movimiento:
    #   -Incluir un texto con la pregunta
    #   -Incluir un boton aceptar que hace la eliminicion y vuelve al listado (con mensaje flash)
    #   -Incluir un boton cancelar que vuelve al inicio SIN eliminar el movimiento
    return render_template("borrado.html", resultado=ha_ido_bien)


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def actualizar(id):
    if request.method == "GET":
        db = DBManager(RUTA)
        movimiento = db.obtenerMovimiento(id)
        formulario = MovimientoForm(data=movimiento)
        return render_template("form_movimiento.html", form=formulario, id=id)
    if request.method == "POST":
        form = MovimientoForm(data=request.form)
        if form.validate():
            db = DBManager(RUTA)
            consulta = "UPDATE movimientos SET fecha=?, concepto=?, tipo=?, cantidad=? where id=?"
            parametros = (
                form.fecha.data,
                form.concepto.data,
                form.tipo.data,
                float(form.cantidad.data),
                form.id.data,
            )
            resultado = db.consultaConParametros(consulta, parametros)

            # Otra alternativa
            # parametros = (
            #     form.fecha.data,
            #     form.concepto.data,
            #     form.tipo.data,
            #     float(form.cantidad.data),
            #     form.id.data,
            # )
            # (fecha, concepto, tipo, cantidad, id) = parametros
            # resultado = db.modificar(fecha, concepto, tipo, cantidad, id)

            if resultado:
                flash("EL movimiento se ha actualizado correctamente", category="Exito")
                return redirect(url_for("home"))
            return "El movimiento no se ha podido guardar en la base de datos."
        else:
            # TODO: pintar los mensajes de error junto al campo que lo provoca
            errores = []
            for key in form.errors:
                errores.append((key, form.errors[key]))

            return render_template(
                "form_movimiento.html", form=form, id=id, errors=errores
            )
