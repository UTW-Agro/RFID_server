import pymysql
from config import config
from services.logger import logger


class BBDD:
    def __init__(self):
        self.connection = pymysql.connect(
            host=config['bbdd']['host'],
            port=config['bbdd']['port'],
            user=config['bbdd']['user'],
            password=config['bbdd']['password'],
            database=config['bbdd']['database'],
            autocommit=True
        )
        self.cursor = self.connection.cursor(cursor=pymysql.cursors.DictCursor)

    def close_connection(self):
        logger.info('solicitado cerrar conexión con la base de datos')
        try:
            self.connection.close()
        except Exception as e:
            logger.error(f'error cerrando conexión con la base de datos: {e}')
            return {"code": 1, "error": e}

    def insert_registro(self, id, timestamp, oficina):
        logger.info(
            f'solicitado añadir registro a la base de datos',
            color="amarillo"
        )
        cmd = f"""
            INSERT INTO registros (timestamp, id, oficina) 
            VALUES ("{timestamp}", "{id}", "{oficina}");
        """
        try:
            self.cursor.execute(cmd)
            result = self.cursor.fetchall()
        except Exception as e:
            logger.error(f'error ejecutando comando {cmd} en la bbdd: {e}')
            return {"code": 1, "error": f'error ejecutando comando {cmd} en la bbdd: {e}'}

        logger.info(f'registro añadido correctamente a la base de datos', color='azul')
        return {"code": 0, "error": ''}

    def registros(self, client):
        logger.info(
            f'solicitando registros a la base de datos',
            color="amarillo"
        )

        cmd = ''
        if client == 'julio' or client == 'jesus':
            logger.info(
                f'solicitando id de todos los usuarios a la base de datos',
                color="blanco"
            )

            cmd_0 = f'SELECT * FROM RFID.nombres;'

            try:
                self.cursor.execute(cmd_0)
                ids = self.cursor.fetchall()
            except Exception as e:
                logger.error(f'error ejecutando comando {cmd_0} en la bbdd: {e}')
                return {
                    "code": 1,
                    "error": f'error ejecutando comando {cmd_0} en la bbdd: {e}',
                    "result": ''
                }

            res = []
            for element in ids:
                cmd = f'SELECT * FROM RFID.registros WHERE id ="{element["id"]}";'
                try:
                    self.cursor.execute(cmd)
                    result = self.cursor.fetchall()
                except Exception as e:
                    logger.error(f'error ejecutando comando {cmd} en la bbdd: {e}')
                    return {
                        "code": 1,
                        "error": f'error ejecutando comando {cmd} en la bbdd: {e}',
                        "result": ''
                    }
                res.append({element['nombre']: result})

            logger.info(f'registros obtenidos correctamente', color='azul')
            return {
                "code": 0,
                "error": '',
                "result": res
            }

        else:
            logger.info(
                f'solicitando id del usuario a la base de datos',
                color="blanco"
            )

            cmd_0 = f'SELECT * FROM RFID.nombres WHERE nombre ="{client}";'

            try:
                self.cursor.execute(cmd_0)
                id = self.cursor.fetchall()[0]['id']
            except Exception as e:
                logger.error(f'error ejecutando comando {cmd_0} en la bbdd: {e}')
                return {
                    "code": 1,
                    "error": f'error ejecutando comando {cmd_0} en la bbdd: {e}',
                    "result": ''
                }

            cmd = f'SELECT * FROM RFID.registros WHERE id ="{id}";'

            try:
                self.cursor.execute(cmd)
                result = self.cursor.fetchall()
            except Exception as e:
                logger.error(f'error ejecutando comando {cmd} en la bbdd: {e}')
                return {
                    "code": 1,
                    "error": f'error ejecutando comando {cmd} en la bbdd: {e}',
                    "result": ''
                }

            logger.info(f'registros obtenidos correctamente', color='azul')
            return {
                "code": 0,
                "error": '',
                "result": result
            }


bbdd = BBDD()
