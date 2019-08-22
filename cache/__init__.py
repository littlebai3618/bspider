# @Time    : 2019-07-31 16:59
# @Author  : 白尚林
# @File    : __init__.py
# @Use     :
import asyncio
import aiomysql
from aiomysql import DictCursor

from config.frame_settings import WEB_STUDIO_DB
from util.tools import coroutine_result


async def test_example(loop):
    pool = coroutine_result(aiomysql.create_pool(
                host=WEB_STUDIO_DB['MYSQL_HOST'],
                port=WEB_STUDIO_DB['MYSQL_PORT'],
                user=WEB_STUDIO_DB['MYSQL_USER'],
                password=WEB_STUDIO_DB['MYSQL_PASSWD'],
                db=WEB_STUDIO_DB['MYSQL_DB'],
                cursorclass=DictCursor
            ))
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT 42;")
            print(cur.description)
            (r,) = await cur.fetchone()
            assert r == 42
    pool.close()
    await pool.wait_closed()


loop = asyncio.get_event_loop()
loop.run_until_complete(test_example(loop))