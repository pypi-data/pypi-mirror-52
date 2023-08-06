import asyncio
from itertools import chain
import json

from aiohttp import ClientSession


ACCESS_TOKEN = '8ad9171c2270c2620b1773e2bea49e735eabc9f334bfcd3b9b1b2c1916316e95'
BASE_URL = 'https://api.wootric.com/v1/responses?access_token=%(access_token)s'
KEYS = ['id', 'end_user_id', 'ip_address', 'origin_url', 'score', 'survey_id']


async def fetch_page(page_num, session, access_token):
    url = BASE_URL % {'access_token': access_token}
    async with session.get(url) as response:
        return json.loads(await response.read())


def pick(d, keys):
    return {k: d[k] for k in keys}


async def run(access_token):
    async with ClientSession() as session:
        tasks = (
            asyncio.Task(fetch_page(page_num, session, access_token))
            for page_num in range(30)
        )
        responses = await asyncio.gather(*tasks)
        data = [pick(response, KEYS) for response in chain.from_iterable(responses)]
    return data


loop = asyncio.get_event_loop()
future = asyncio.ensure_future(run(ACCESS_TOKEN))
data = loop.run_until_complete(future)
scores = [d['score'] for d in data]
print(sum(scores) / len(scores))
