from aiohttp import web
from aiopg.sa import create_engine


async def hello(request):
    return web.Response(text="Hello, world")


async def health(request):
    return web.Response(text="ok", status=200, content_type='text/plain')


async def pg_init(app):
    app['pg'] = await create_engine(
        dsn='dbname={db} user={user} password={password} host={host} port={port}'.format(
            db='manager_test',
            user='manager',
            password='manager',
            host='localhost',
            port=5432
        )
    )


async def pg_close(app):
    app['pg'].close()
    await app['pg'].wait_closed()


def get_app():
    app = web.Application()

    app.on_startup.append(pg_init)
    app.on_cleanup.append(pg_close)

    app.add_routes([web.get('/', hello)])
    app.add_routes([web.get('/health', health)])

    return app


if __name__ == '__main__':
    web.run_app(get_app(), port=8080, host='0.0.0.0')
