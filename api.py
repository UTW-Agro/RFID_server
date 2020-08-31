from aiohttp import web
from cors import cors_factory
from auth import BasicAuthMiddleware
from services.logger import logger
from config import config
from routes.nuevo_registro import insert
from services.sql import bbdd

auth = BasicAuthMiddleware()


@auth.required
async def get_registros(request):
    r = bbdd.registros(auth.user)
    if r["code"] == 0:
        res = r['result']
        return web.json_response(res, status=200)
    elif r["code"] == 1:
        return web.Response(status=500, text=r["error"])
    else:
        return web.Response(status=400, text=r["error"])


@auth.required
async def update_registro(request):
    logger.info('solicitado endpoint de insertar un nuevo registro')
    params = await request.json()
    if 'id' not in params:
        logger.warning(f'no se ha pasado el parametro id')
        return web.Response(status=400, text=f'el parametro id es obligatorio')
    if auth.user == 'rasp':
        r = insert(params['id'])
    else:
        r = insert(params['id'], oficina=0)
    if r != 0:
        logger.warning(f'ha ocurido un error insertando registo en la base de datos: {r}')
        return web.Response(status=500, text=f'error interno insertando registro en la base de datos')

    return web.Response(status=200, text='registro guardado correctamente')



@auth.required
async def ok(request):
    return web.Response()


app = web.Application(middlewares=[cors_factory, auth])
app.add_routes([
    web.get('/ok', ok),
    web.get('/registros', get_registros),
    web.post('/registro', update_registro)
])

web.run_app(app, host='163.117.205.77', port=config['server']['port'])
