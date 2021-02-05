import pytest

from server import get_app


@pytest.fixture
def cli(loop, aiohttp_client):
    app = get_app()
    return loop.run_until_complete(aiohttp_client(app))


async def test_hello(cli):
    resp = await cli.get('/')
    assert resp.status == 200
