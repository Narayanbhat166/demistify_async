from time import sleep
import aiohttp
import asyncio


async def make_request(url, session):
    response = await session.get(url)
    data = await response.json()
    # Danger zone
    # sleep(1)
    print(url, "Done")
    return data


async def main():
    async with aiohttp.ClientSession() as session:

        posts = await make_request("https://jsonplaceholder.typicode.com/posts", session)

        tasks = []

        for post in posts[:10]:
            post_id = post.get('id')
            comments_url = f"https://jsonplaceholder.typicode.com/posts/{post_id}/comments"

            task = make_request(comments_url, session)
            tasks.append(task)

        await asyncio.gather(*tasks)

asyncio.run(main())
