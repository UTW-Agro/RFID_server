from services.logger import logger
from services.sql import bbdd
from datetime import datetime


def insert(id, oficina=1):
    try:
        t = str(datetime.now())
        bbdd.insert_registro(id, t, oficina)
    except Exception as err:
        return err

    return 0
