import sqlite3


class DBManager:
    """
    SELECT id, fecha, concepto, tipo, cantidad FROM movimientos
    """

    def __init__(self, ruta):
        self.ruta = ruta

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
        self.movimientos = []
        nombres_columnas = []
        for columna in cursor.description:
            nombres_columnas.append(columna[0])
        for dato in datos:
            movimiento = {}
            indice = 0
            for nombre in nombres_columnas:
                movimiento[nombre] = dato[indice]
                indice += 1
            self.movimientos.append(movimiento)

        # 5. Cerrar la conexion
        conexion.close()

        # 6. Devolver los resultados
        return self.movimientos
