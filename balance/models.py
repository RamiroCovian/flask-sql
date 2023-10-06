from datetime import date
import sqlite3


class DBManager:
    """
    SELECT id, fecha, concepto, tipo, cantidad FROM movimientos
    """

    def __init__(self, ruta):
        self.ruta = ruta

    def conectar(self):
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        return conexion, cursor

    def desconectar(self, conexion):
        conexion.close()

    def consultaSQL(self, consulta):
        # 1. Conectar a la base de datos
        conexion = sqlite3.connect(self.ruta)

        # 2. Abrir un cursor
        cursor = conexion.cursor()

        # 3. Ejecutar la consulta
        cursor.execute(consulta)

        # 4. Tratar los datos
        # 4.1 Obtener los datos
        datos = cursor.fetchall()

        # 4.2 Los guardo localmente
        self.registros = []
        nombres_columnas = []
        for columna in cursor.description:
            nombres_columnas.append(columna[0])
        for dato in datos:
            movimiento = {}
            indice = 0
            for nombre in nombres_columnas:
                movimiento[nombre] = dato[indice]
                indice += 1
            self.registros.append(movimiento)

        # 5. Cerrar la conexion
        conexion.close()

        # 6. Devolver los resultados
        return self.registros

    def obtenerMovimiento(self, id):
        consulta = (
            "SELECT id, fecha, concepto, tipo, cantidad FROM movimientos WHERE id=?"
        )
        conexion, cursor = self.conectar()
        cursor.execute(consulta, (id,))
        datos = cursor.fetchone()
        resultado = None
        if datos:
            nombres_columnas = []
            for columna in cursor.description:
                nombres_columnas.append(columna[0])
            movimiento = {}
            indice = 0
            for nombre in nombres_columnas:
                movimiento[nombre] = datos[indice]
                indice += 1
            movimiento["fecha"] = date.fromisoformat(movimiento["fecha"])
            resultado = movimiento

        self.desconectar(conexion)
        return resultado

    def consultaConParametros(self, consulta, parametros):
        conexion, cursor = self.conectar()

        resultado = False
        try:
            cursor.execute(consulta, parametros)
            conexion.commit()
            resultado = True

        except Exception as ex:
            print(ex)
            conexion.rollback()

        self.desconectar(conexion)
        return resultado

    def modificar(self, fecha, concepto, tipo, cantidad, id):
        """
        Es otra opcion de actualizar que utiliza consultaConParametros
        """

        sql = (
            "UPDATE movimientos SET fecha=?, concepto=?, tipo=?, cantidad=? where id=?"
        )
        data = (fecha, concepto, tipo, cantidad, id)
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()

        resultado = False
        try:
            cursor.execute(sql, data)
            conexion.commit()
            resultado = True
        except:
            conexion.rollback()

        conexion.close()
        return resultado

    def crear_movimiento(self, consulta, parametros):
        conexion, cursor = self.conectar()

        resultado = False
        try:
            cursor.execute(consulta, parametros)
            conexion.commit()
            resultado = True
        except Exception as ex:
            print(ex)
            conexion.rollback()

        self.desconectar(conexion)
        return resultado

    def insertar(self, fecha, concepto, tipo, cantidad):
        """
        INSERT INTO movimientos(fecha, concepto, tipo, cantidad) VALUES(?, ?, ?, ?)
        """
        sql = "INSERT INTO movimientos(fecha, concepto, tipo, cantidad) VALUES(?, ?, ?, ?)"
        data = (fecha, concepto, tipo, cantidad)
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()

        resultado = False
        try:
            cursor.execute(sql, data)
            conexion.commit()
            resultado = True
        except:
            conexion.rollback()

        conexion.close()
        return resultado

    def borrar(self, id):
        """
        DELETE FROM movimientos WHERE id=?
        """
        sql = f"DELETE FROM movimientos WHERE id=?"
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()

        resultado = False
        try:
            cursor.execute(sql, (id,))
            conexion.commit()
            resultado = True
        except:
            conexion.rollback()

        conexion.close()
        return resultado
